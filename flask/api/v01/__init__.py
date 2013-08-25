'''
Created on Jul 3, 2013

@author: pussbb
'''
from flask.views import MethodView
from .. import db

from ..output import output_response

from flask import request
import json
from werkzeug.exceptions import MethodNotAllowed
from werkzeug.exceptions import NotImplemented as HTTPNotImplemented

from sqlalchemy.orm import joinedload_all
from sqlalchemy import desc
from wtforms import Form

def allowed_methods(methods):
    def real_wrapper(func):
        def wrapper(*args, **kwargs):
            if request.method not in methods:
                raise MethodNotAllowed()
            return func(*args, **kwargs)
        return wrapper
    return real_wrapper

class Command(MethodView):

    TABLE = None
    REPLY_SUCCESS = {
                      'total': 0,
                      'page': 0,
                      'per_page': 20,
                      'records': [],
                   }

    FORM = Form

    ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'DELETE']

    URI = None
    PK = 'pk'
    PK_TYPE = 'int'

    def dispatch_request(self, *args, **kwargs):
        key_value = kwargs.get(Command.PK)
        if isinstance(key_value, basestring):
            return self.custom_func(key_value)

        if request.method not in self.ALLOWED_METHODS:
            self.not_allowed()
        return MethodView.dispatch_request(self, *args, **kwargs)

    def get(self, pk):

        query = self.__query()

        #load relations
        if 'with' in request.values:
            names = json.loads(request.values['with'] or '[]')
            query = Command.__with(query, names)

        #find record by id
        if pk:
            record = query.filter_by(id = pk).first_or_404()
            return output_response(record.serialize())

        if 'filter' in request.values:
            filter_args = json.loads(request.values['filter'] or '{}')
            query = self.__filter(query, filter_args)

        if 'order_by' in request.values:
            parts = request.values['order_by'].replace('"', '').split()
            query = self.__order_by(query, parts)

        #get records
        records = query.paginate(Command.page(), Command.per_page())

        reply = self.REPLY_SUCCESS.copy()
        reply['records'] = [i.serialize() for i in records.items]
        reply['total'] = records.total
        reply['page'] = records.page
        reply['per_page'] = records.per_page
        return output_response(reply)

    def post(self):
        model = self.TABLE(**request.form.to_dict())

        form = self.FORM(request.form, model)
        if not form.validate():
            return output_response({'erorrs': form.errors}, 400)

        db.session.add(model)
        db.session.commit()
        return output_response(model.serialize(), 201)

    def delete(self, pk):
        count = self.__query().filter_by(id = pk).delete()
        if count == 0:
            return output_response({'erorrs': ['Could not delete']}, 400)
        return output_response({'total': count}, 204)

    def put(self, pk):
        model = self.__query().filter_by(id = pk).first_or_404()

        for item, value in request.form.iteritems():
            setattr(model, item, value)

        form = self.FORM(request.form, model)
        if not form.validate():
            return output_response({'erorrs': form.errors})

        return output_response(model.serialize())

    def __query(self):
        return self.TABLE.query

    @staticmethod
    def not_allowed():
        raise MethodNotAllowed()

    def custom_func(self, func_name):
        func = getattr(self, func_name, None)
        if not func:
            raise HTTPNotImplemented()
        return func()

    def __filter(self, query, filter_args):
        for item, value in filter_args.items():
            field = getattr(self.TABLE, item)
            if isinstance(value, list):
                query = query.filter(field.in_(value))
                continue
            if isinstance(value, dict):
                query = Command.__filter_by_condition(field, value, query)
                continue
            query = query.filter(field == value)
        return query

    def __order_by(self, query, args):
        field = getattr(self.TABLE, args[0])
        if args[-1] == 'desc':
            field = desc(field)
        return query.order_by(field)

    @staticmethod
    def __filter_by_condition(field, condition, query):

        comparison = condition['comparison_key']
        value =  condition['value']

        if comparison in ('<>', '!='):
            if value is None:
                query = query.filter( field != None )
            if isinstance(value, list):
                query = ~query.filter(field.in_(value))
            query = query.filter(field != value)
        elif comparison == '<':
            query = query.filter(field < value)
        elif comparison == '>':
            query = query.filter(field > value)
        elif comparison == 'between':
            query = query.filter(field.between(value[0], value[1]))

        return query

    @staticmethod
    def __with(query, relations):
        return query.options(joinedload_all(*relations))

    @staticmethod
    def page():
        if 'page' in request.values:
            return int(request.values['page'])
        return 1

    @staticmethod
    def per_page():
        if 'per_page' in request.values:
            return int(request.values['per_page'])
        return 20


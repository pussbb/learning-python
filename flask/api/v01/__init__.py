'''
Created on Jul 3, 2013

@author: pussbb
'''
from flask.views import MethodView
from .. import json_responce, db
from flask import request
import json
from werkzeug.exceptions import MethodNotAllowed, NotImplemented

from sqlalchemy.orm import joinedload_all
from sqlalchemy import desc

class Command(MethodView):

    TABLE = None
    REPLY_SUCCESS = {
                      'total': 0,
                      'page': 0,
                      'per_page': 20,
                      'records': [],
                   }

    """
        List of allowed methods that can be performed on the object
        e.g. 
        ALLOWED_METHODS = ['GET'] - allow only get data nothing else
    """
    ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'DELETE']
    URI = None
    PK = 'pk'
    PK_TYPE = 'int'

    def dispatch_request(self, *args, **kwargs):
        if request.method not in self.ALLOWED_METHODS:
            self.not_allowed()
        return MethodView.dispatch_request(self, *args, **kwargs)

    def get(self, pk):

        # custom function
        if isinstance(pk, basestring):
            return self.custom_func(pk)
        query = self.__query()
        query = self.__with(query)

        #find record by id
        if pk:
            record = query.filter_by(id = pk).first_or_404()
            return json_responce(record.serialize())

        #return all records
        query = self.__filter(query)
        query = self.__order_by(query)
        print str(query)
        records = query.paginate(self.page(), self.per_page())

        reply = self.REPLY_SUCCESS.copy()
        reply['records'] = [i.serialize() for i in records.items]
        reply['total'] = records.total
        reply['page'] = records.page
        reply['per_page'] = records.per_page
        return json_responce(reply)

    def post(self):
        model = self.TABLE(**request.form.to_dict())
        db.session.add(model)
        db.session.commit()
        return json_responce(model.serialize())

    def delete(self, pk):
        r = self.__query().filter_by(id = pk).delete()
        return json_responce({'total': r})

    def put(self, pk):
        model = self.__query().filter_by(id = pk).first_or_404()
        for i,v in request.form.iteritems():
            setattr(model, i, v)
        return json_responce(model.serialize())

    def not_allowed(self):
        raise MethodNotAllowed()

    def custom_func(self, func_name):
        func = getattr(self, func_name, None)
        if not func:
            raise NotImplemented()
        return func()

    def __filter(self, query):
        if 'filter' not in request.args:
            return query
        filter_args = json.loads(request.args['filter'] or '{}')
        for i,v in filter_args.items():
            field = getattr(self.TABLE, i)
            if isinstance(v, list):
                query = query.filter(field.in_(v))
                continue
            if isinstance(v, dict):
                query = self.__filter_by_condition(field, v, query)
                continue
            query = query.filter(field == v)
        return query

    def __filter_by_condition(self, field, condition, query):
        comparison = condition['comparison_key']
        value =  condition['value']
        if comparison in ('<>', '!='):
            if value is None:
                return query.filter( field != None )
            if isinstance(value, list):
                return ~query.filter( field.in_(value))
            return query.filter(field != value)
        if comparison == '<':
            return query.filter( field < value)
        if comparison == '>':
            return query.filter( field > value)
        if comparison == 'between':
            return query.filter(field.between(value[0], value[1]))
        return query

    def __with(self, query):
        if 'with' not in request.args:
            return query
        relations = json.loads(request.args['with'] or '[]')
        return query.options(joinedload_all(*relations))

    def __order_by(self, query):
        if 'order_by' not in request.args:
            return query

        parts = request.args['order_by'].replace('"', '').split()
        field = getattr(self.TABLE, parts[0])
        if parts[-1] == 'desc': 
            field = desc(field) 
        return query.order_by(field)


    def page(self):
        if 'page' in request.args:
            return int(request.args['page'])
        return 1
    
    def per_page(self):
        if 'per_page' in request.args:
            return int(request.args['per_page'])
        return 20

    def __query(self):
        return self.TABLE.query


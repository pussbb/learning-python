'''
Created on Jul 3, 2013

@author: pussbb
'''
from flask.views import MethodView
from .. import json_responce, db
from flask import request

from werkzeug.exceptions import MethodNotAllowed, NotImplemented


class Command(MethodView):
    TABLE = None
    REPLY_SUCCESS = {'records': [], 'count': 0, 'page': 0}
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
        #find record by id
        if pk:
            record = self.TABLE.query.filter_by(id = pk).first_or_404()
            return json_responce(record.serialize())
        #return all records
        records = self.TABLE.query.all()
        reply = self.REPLY_SUCCESS.copy()
        reply['records'] = [i.serialize() for i in records]
        return json_responce(reply)

    def post(self):
        model = self.TABLE(**request.form.to_dict())
        db.session.add(model)
        db.session.commit()
        return json_responce(model.serialize())

    def delete(self, pk):
        r = self.TABLE.query.filter_by(id = pk).delete()
        return json_responce({'total': r})

    def put(self, pk):
        model = self.TABLE.query.filter_by(id = pk).first_or_404()
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

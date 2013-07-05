'''
Created on Jul 3, 2013

@author: pussbb
'''
from flask.views import MethodView
from .. import json_responce, db
from flask import request

class Command(MethodView):
    TABLE = None
    REPLY_SUCCESS = {'records': [], 'count': 0, 'page': 0}
    URI = None
    PK = 'pk'
    PK_TYPE = 'int'

    def get(self, pk): 
        if pk:
            record = self.TABLE.query.filter_by(id = pk).first_or_404()
            return json_responce(record.serialize())
        records = self.TABLE.query.all()
        reply = self.REPLY_SUCCESS.copy()
        reply['records'] = [i.serialize() for i in records]
        return json_responce(reply)

    def post(self):
        pass

    def delete(self, pk):
        r = self.TABLE.query.filter_by(id = pk).delete()
        return json_responce({'total': r})

    def put(self, pk):
        model = self.TABLE.query.filter_by(id = pk).first_or_404()
        for i,v in request.form.iteritems():
            setattr(model, i, v)
        return json_responce(model.serialize())
        #user.save()



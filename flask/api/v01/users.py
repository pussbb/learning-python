'''
Created on Jul 3, 2013

@author: pussbb
'''

from .. import json_responce


from flask.views import MethodView

class Users(MethodView):
    URI = 'users'
    PK = 'user_id'
    PK_TYPE = 'int'

    def get(self, user_id): 
        print user_id
        return json_responce({'id':user_id})
    
    def post(self):
        return json_responce({'id':9090})
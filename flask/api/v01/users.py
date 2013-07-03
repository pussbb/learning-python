'''
Created on Jul 3, 2013

@author: pussbb
'''

from .. import json_responce


from flask.views import MethodView
from flask import request
"""
  Get User
"""
class Users(MethodView):
    URI = 'users'
    PK = 'user_id'
    PK_TYPE = 'int'

    def get(self, user_id): 
        return json_responce({'id':user_id})
    
    def post(self):
        return json_responce(request.form.to_dict())
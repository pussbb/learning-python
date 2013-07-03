'''
Created on Jul 3, 2013

@author: pussbb
'''

from .. import json_responce


from flask.views import MethodView

class Users(MethodView): 
    methods = ['GET', 'POST', 'PUT']

    def get(self, uuid): 
        return json_responce({'id':uuid})
    
    def __repr__(self):
        return self.__class__.__name__.lower()
'''
Created on Jul 3, 2013

@author: pussbb
'''

from .. import json_responce, request

from ..models.user import User
from . import Command

"""
  Get User
"""

class Users(Command):
    URI = 'users'
    TABLE = User

    def post(self):
        return json_responce(request.form.to_dict())

    def delete(self, pk): pass

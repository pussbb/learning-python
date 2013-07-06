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

    def delete(self, pk): pass

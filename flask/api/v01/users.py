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
# The auto-magic version
# I pulled this off a blog, forget the source.


class Users(Command):
    URI = 'users'
    TABLE = User

    def post(self):
        return json_responce(request.form.to_dict())
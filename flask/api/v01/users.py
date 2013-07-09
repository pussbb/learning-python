'''
Created on Jul 3, 2013

@author: pussbb
'''

from ..models.user import User
from . import Command

from wtforms import Form
from wtforms import validators, TextField

"""
  Get User
"""

# http://flask.pocoo.org/snippets/64/
class UserForm(Form):
    email = TextField('email', [validators.Email()])

class Users(Command):
    URI = 'users'
    TABLE = User
    FORM = UserForm

    def me(self):
        return 'hello me'

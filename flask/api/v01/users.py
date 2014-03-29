'''
Created on Jul 3, 2013

@author: pussbb
'''

from ..models.user import User
from . import Command, allowed_methods

from wtforms import Form
from wtforms import validators, StringField

"""
Get User
"""


# http://flask.pocoo.org/snippets/64/
class UserForm(Form):
    email = StringField('email', [validators.Email()])


class Users(Command):
    URI = 'users'
    TABLE = User
    FORM = UserForm

    @allowed_methods(['GET', 'POST', ])
    def me(self):
        return "hello me <xmp>%s</xmp>" % repr(self)


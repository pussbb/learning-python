'''
Created on Jul 3, 2013

@author: pussbb
'''

from ..models.user import User
from . import Command, allowed_methods

from wtforms import validators, StringField
from wtforms_alchemy import ModelForm

"""
Get User
"""


# http://flask.pocoo.org/snippets/64/
class UserForm(ModelForm):

    email = StringField('email', [validators.Email()])


    class Meta:
        model = User


class Users(Command):
    """Get all users from system

    """

    URI = 'users'
    TABLE = User
    FORM = UserForm

    @allowed_methods(['GET', 'POST', ])
    def me(self):
        """sdasdas

        """
        return "hello me <xmp>%s</xmp>" % repr(self)


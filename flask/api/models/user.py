'''
Created on Jul 4, 2013

@author: pussbb
'''

from . import BaseModel
from api import db

from sqlalchemy.orm import validates

import hashlib

class User(BaseModel, db.Model):
    '''
    classdocs
    '''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=True)
    _password = db.Column('password', db.String(20))
    api_key = db.Column(db.String(150))
    #_length = db.Column(db.Integer)

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

    """
    http://docs.sqlalchemy.org/en/latest/orm/mapper_config.html#using-descriptors-and-hybrids
    """

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = hashlib.md5('password').hexdigest()




'''
Created on Jul 4, 2013

@author: pussbb
'''

from . import BaseModel
from api import db

from sqlalchemy.orm import validates, MapperExtension, mapper

import hashlib
import uuid
import json

class UserMapperExtension(MapperExtension):

    def before_insert(self, mapper, connection, instance):
        if not instance.api_key:
            instance.api_key  = str(uuid.uuid1()).replace('-','')

    def before_update(self, mapper, connection, instance): pass

class User(BaseModel, db.Model):
    '''
    classdocs
    '''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    login = db.Column(db.String(120), unique = True, nullable = False)
    _password = db.Column('password', db.String(20), nullable = False)
    role_id = db.Column(db.Integer)
    api_key = db.Column(db.String(150))
    _meta_data = db.Column('meta_data',db.Text, default='[]')

    __mapper_args__ = { 'extension': UserMapperExtension() }

    __table_args__ = (
                      db.UniqueConstraint('email', 'login', name='_email_login_uc'),
                      )

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
    def password(self, pswd):
        if pswd == self._password:
            return
        self._password = hashlib.md5(str(pswd)).hexdigest()

    @property
    def meta_data(self):
        if self._meta_data is None:
            return []
        return json.loads(self._meta_data)

    @meta_data.setter
    def meta_data(self, meta_data):
        if not isinstance(meta_data, basestring):
            meta_data = json.dumps(meta_data)
        self._meta_data = meta_data


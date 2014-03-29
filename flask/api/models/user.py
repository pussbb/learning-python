'''
Created on Jul 4, 2013

@author: pussbb
'''

from . import BaseModel
from api import DB

from sqlalchemy.orm import MapperExtension
from sqlalchemy import Column, Integer, String, Text

import hashlib
import uuid
import json


class UserMapperExtension(MapperExtension):

    def before_insert(self, mapper, connection, instance):
        if not instance.api_key:
            instance.api_key  = str(uuid.uuid1()).replace('-', '')


class User(BaseModel, DB.Model):
    """
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    login = Column(String(120), unique=True, nullable=False)
    _password = Column('password', String(20), nullable=False)
    role_id = Column(Integer)
    api_key = Column(String(150))
    _meta_data = Column('meta_data', Text, default='[]')

    __mapper_args__ = { 'extension': UserMapperExtension()}

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
        return json.loads(self._meta_data or '[]')

    @meta_data.setter
    def meta_data(self, meta_data):
        if not isinstance(meta_data, [dict, list]):
            meta_data = json.dumps(meta_data)
        self._meta_data = meta_data


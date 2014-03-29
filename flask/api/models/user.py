'''
Created on Jul 4, 2013

@author: pussbb
'''

from . import BaseModel
from .. import DB

from sqlalchemy.orm import mapper
from sqlalchemy import event
from sqlalchemy import Column, Integer, String, Text

import hashlib
import uuid
import json


class User(BaseModel, DB.Model):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    login = Column(String(120), unique=True, nullable=False)
    _password = Column('password', String(20), nullable=False)
    role_id = Column(Integer)
    api_key = Column(String(150))
    _meta_data = Column('meta_data', Text, default='[]')

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
        self._password = hashlib.md5(pswd.encode('utf8')).hexdigest()

    @property
    def meta_data(self):
        return json.loads(self._meta_data or '[]')

    @meta_data.setter
    def meta_data(self, meta_data):
        if not isinstance(meta_data, [dict, list]):
            meta_data = json.dumps(meta_data)
        self._meta_data = meta_data


def check_meta_data_field(data):
    print(data.id)
    if isinstance(data._meta_data, (list, dict)):
        data._meta_data = json.dumps(data._meta_data)

def before_user_insert(mapper, connection, target):
    if not target.api_key:
        target.api_key = str(uuid.uuid1()).replace('-', '')
    if target._meta_data is None:
        target._meta_data = []
    check_meta_data_field(target)

def before_user_update(mapper, connection, target):
    print('before update')
    check_meta_data_field(target)

event.listen(User, 'before_insert', before_user_insert)
event.listen(User, 'before_update', before_user_update)

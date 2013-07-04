'''
Created on Jul 4, 2013

@author: pussbb
'''

from . import BaseModel
from .. import db


class User(BaseModel, db.Model):
    '''
    classdocs
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(20))

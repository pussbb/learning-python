'''
Created on Jul 4, 2013

@author: pussbb
'''

from .. import db

class BaseModel(object):

    PK_KEY = 'id'

    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

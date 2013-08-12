'''
Created on Jul 4, 2013

@author: pussbb
'''

import datetime
from decimal import Decimal

class BaseModel(object):

    EXTRA_FIELDS = []

    def __init__(self, **kwargs):
        for i,v in kwargs.items():
            setattr(self, i, v)

    def serialize(self):
        result = {}
        for c in self.__table__.columns:
            result[c.name] = self.__get_attr(c.name)
            self._append_relations(c, result)

        for field in self.EXTRA_FIELDS:
            result[field] = self.__get_attr(field)
        return result

    def _append_relations(self, column, result):
        for i in column.foreign_keys:
            if i.name not in self.__dict__:
                continue
            data = self.__dict__[i.name]
            if not data:
                result[i.name] = data
            elif isinstance(data, BaseModel):
                result[i.name] = data.serialize()
            else:
                result[i.name] = [i.serialize() for i in data]

    def __get_attr(self, attr):
        value = getattr(self, attr)
        if type(value) in (datetime.datetime, datetime.date, Decimal) :
            return str(value)
        return value


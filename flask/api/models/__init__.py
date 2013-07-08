'''
Created on Jul 4, 2013

@author: pussbb
'''

import datetime
from decimal import Decimal

class BaseModel(object):

    EXTRA_FIELDS = []

    """
        http://pythonhosted.org/Flask-SQLAlchemy/binds.html
    """

    def __init__(self, **kwargs):
        for i,v in kwargs.items():
            setattr(self, i, v)

    def serialize(self):
        result = {}
        for c in self.__table__.columns:
            result[c.name] = self.__get_attr(c.name)
            result.update(self._append_relations(c))

        for field in self.EXTRA_FIELDS:
            result[field] = self.__get_attr(field)
        return result

    def _append_relations(self, column):
        result = {}
        if not column.foreign_keys:
            return result

        for i in column.foreign_keys:
            if i.name not in self.__dict__:
                continue

            relation = self.__dict__[i.name]
            if relation is None:
                result[i.name] = None
                continue

            if isinstance(relation, BaseModel):
                result[i.name] = relation.serialize()
            else:
                result[i.name] = [i.serialize() for i in relation]

        return result

    def __get_attr(self, attr):
        value = getattr(self, attr)
        if type(value) in(datetime.datetime, datetime.date, Decimal):
            return str(value)
        return value


'''
Created on Jul 4, 2013

@author: pussbb
'''

class BaseModel(object):

    PK_KEY = 'id'
    
    """
        http://pythonhosted.org/Flask-SQLAlchemy/binds.html
    """
    __bind_key__ = 'db1'

    def __init__(self, **kargv):
        for i,v in kargv:
            setattr(self, i, v)

    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

"""
Created on Jul 7, 2013
@author: pussbb

"""

from . import BaseModel
from .user import User
from api import DB
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import BigInteger, DateTime, Text
from sqlalchemy.orm import relationship

class News(BaseModel, DB.Model):

    __tablename__ = 'news'

    EXTRA_FIELDS = ['content_length',]

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    link = Column(String(255), nullable=False)

    author_id = Column(BigInteger, ForeignKey('users.id', name="author"))
    author = relationship(User, uselist=False) #, lazy="joined"

    content = Column(Text())
    created_at = Column(DateTime, server_default='NOW()')

    @property
    def content_length(self):
        return len(self.content)

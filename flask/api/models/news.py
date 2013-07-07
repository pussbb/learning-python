'''
Created on Jul 7, 2013

@author: pussbb
'''

from . import BaseModel
from .user import User
from .. import db


class News(BaseModel, db.Model):

    __tablename__ = 'news'

    EXTRA_FIELDS = ['content_length',]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)

    author_id = db.Column(db.BigInteger, db.ForeignKey('users.id', name="author"))
    author =  db.relationship(User, uselist=False , lazy="joined" )

    content = db.Column(db.Text())
    created_at = db.Column(db.DateTime, server_default='NOW()')

    @property
    def content_length(self):
        return len(self.content)

'''


@author: pussbb
'''

from . import BaseModel
from .. import db
from sqlalchemy import Column, Integer, String

class Language(BaseModel, db.Model):

    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False)
    locale = Column(String(50), nullable=False)
    name = Column(String(150), nullable=False)

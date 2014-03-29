"""
@author: pussbb

"""

from . import BaseModel
from api import DB
from sqlalchemy import Column, Integer, String


class Language(BaseModel, DB.Model):

    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False)
    locale = Column(String(50), nullable=False)
    name = Column(String(150), nullable=False)

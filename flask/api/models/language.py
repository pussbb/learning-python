'''


@author: pussbb
'''

from . import BaseModel
from .. import db


class Language(BaseModel, db.Model):

    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    locale = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(150), nullable=False)

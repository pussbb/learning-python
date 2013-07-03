'''
Created on Jul 3, 2013

@author: pussbb
'''
from flask import Blueprint
from .. import json_responce

from users import Users

VERSION = 0.1

api = Blueprint('v.0.1', __name__)

commands = [Users()]

@api.route('/')
def index():
    return json_responce({'commands': commands})

for command in commands:
    api.add_url_rule(
                 '/{0}/<int:uuid>'.format(repr(command)),
                  view_func=command.as_view(repr(command)),
                  defaults={'uuid':None}
                  )

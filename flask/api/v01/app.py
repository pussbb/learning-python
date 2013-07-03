'''
Created on Jul 3, 2013

@author: pussbb
'''
from flask import Blueprint
from .. import json_responce
import pydoc

from users import Users

VERSION = 0.1

api = Blueprint('v.0.1', __name__)

commands = [Users]

@api.route('/')
def index():
    result = []
    for command in commands:
        item = {
            'uri': command.URI, 
            'help': pydoc.render_doc(command, title="%s")
        }
        result.append(item)

    return json_responce({'commands': result})

for command in commands:

    func = command.as_view(command.URI)
    api.add_url_rule('/{0}/'.format(command.URI),
                     view_func=func,
                     methods=['POST',])
    api.add_url_rule(
                 '/{0}/<{1}:{2}>'.format(command.URI, command.PK_TYPE,command.PK),
                  view_func=func,
                  methods=['GET', 'PUT', 'DELETE']
                  )


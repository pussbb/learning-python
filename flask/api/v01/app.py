'''
Created on Jul 3, 2013

@author: pussbb
'''
from flask import Blueprint, url_for
from .. import json_responce
import pydoc

from .users import Users
from .languages import Languages

api = Blueprint('v.0.1', __name__, url_prefix='/api/v.0.1')

commands = [Users, Languages]

@api.route('/')
def index():
    result = []
    for command in commands:
        item = {
            'uri': url_for('.{0}'.format(command.URI), _external=True),
            'help': pydoc.render_doc(command)
        }
        result.append(item)

    return json_responce({'commands': result})

for command in commands:
    func = command.as_view(command.URI)

    api.add_url_rule('/{0}/'.format(command.URI),
                     view_func=func,
                     methods=['GET', ], defaults={command.PK:None})

    api.add_url_rule('/{0}/<{1}>'.format(command.URI, command.PK),
                     view_func=func,
                     methods=['GET', ])

    api.add_url_rule('/{0}/'.format(command.URI),
                     view_func=func,
                     methods=['POST', ])

    api.add_url_rule(
                 '/{0}/<{1}:{2}>'.format(command.URI, command.PK_TYPE, command.PK),
                  view_func=func,
                  methods=['GET', 'PUT', 'DELETE']
                  )


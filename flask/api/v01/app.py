'''
Created on Jul 3, 2013

@author: pussbb
'''
from flask import Blueprint, url_for
from .. import json_responce
import pydoc

from .users import Users
from .languages import Languages
from .news import News

api_v01 = Blueprint('v.0.1', __name__, url_prefix='/api/v.0.1')

commands = [Users, Languages, News]

@api_v01.route('/')
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

    api_v01.add_url_rule('/{0}/'.format(command.URI),
                     view_func=func,
                     methods=['GET', ], defaults={command.PK:None})

    api_v01.add_url_rule('/{0}/<{1}>'.format(command.URI, command.PK),
                     view_func=func)

    api_v01.add_url_rule('/{0}/'.format(command.URI),
                     view_func=func,
                     methods=['POST', ])
    rule = '/{0}/<{1}:{2}>'.format(command.URI, command.PK_TYPE, command.PK)
    api_v01.add_url_rule(rule,
                  view_func=func,
                  methods=['GET', 'PUT', 'DELETE']
                  )


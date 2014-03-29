"""
Created on Jul 3, 2013

@author: pussbb
"""


from flask import Blueprint, url_for
from ..output import output_response
import pydoc

from .users import Users
from .languages import Languages
from .news import News

API_V01 = Blueprint('v.0.1', __name__, url_prefix='/api/v.0.1')

_COMMANDS = [Users, Languages, News]


@API_V01.route('/')
def index():
    result = []
    for command in _COMMANDS:
        item = {
            'uri': url_for('.{0}'.format(command.URI), _external=True),
            'help': pydoc.render_doc(command)
        }
        result.append(item)

    return output_response({'commands': result})

for element in _COMMANDS:
    func = element.as_view(element.URI)
    API_V01.add_url_rule('/{0}/'.format(element.URI),
                         view_func=func,
                         methods=['GET', ],
                         defaults={element.PK: None},)

    API_V01.add_url_rule('/{0}/<{1}>'.format(element.URI, element.PK),
                         view_func=func,)

    API_V01.add_url_rule('/{0}/'.format(element.URI),
                         view_func=func, methods=['POST', ])
    rule = '/{0}/<{1}:{2}>'.format(element.URI, element.PK_TYPE, element.PK)
    API_V01.add_url_rule(rule, view_func=func, methods=['GET', 'PUT', 'DELETE'])


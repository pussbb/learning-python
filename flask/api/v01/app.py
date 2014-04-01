"""
Created on Jul 3, 2013

@author: pussbb
"""


from flask import Blueprint, url_for
from ..output import output_response
import inspect

from .users import Users
from .languages import Languages
from .news import News


API_V01 = Blueprint('v_0_1', __name__, url_prefix='/api/v.0.1')

_COMMANDS = [Users, Languages, News]

__ACTION = {
    'url': None,
    'description': None,
    'methods': []
}

__MODULE = {
    'url': None,
    'description': None,
    'uri': None,
    'actions' : []
}


def __get_available_actions(command):
    actions = []
    for method in command.ALLOWED_METHODS:
        action = __ACTION.copy()
        action['methods'] = [str(method)]
        action['description'] = getattr(command, method.lower()).__doc__
        extra = {
            command.PK: '<{0}>'.format(command.PK_TYPE),
            '_external': True
        }
        action['url'] = url_for(".{0}".format(command.URI), **extra)
        actions.append(action)

    for name in command.__dict__:
        item = getattr(command, name)
        if name.startswith('_') or inspect.isclass(item):
            continue
        if not inspect.ismethod(item) and not inspect.isfunction(item):
            continue

        action = __ACTION.copy()
        action['methods'] = []
        action['description'] = item.__doc__
        extra = {command.PK: item.__name__, '_external': True}
        action['url'] = url_for(".{0}".format(command.URI), **extra)
        actions.append(action)

    return actions


@API_V01.route('/')
def index():
    result = []
    for command in _COMMANDS:
        module = __MODULE.copy()
        module['name'] = command.__name__
        module['description'] = command.__doc__
        module['uri'] = command.URI
        module['actions'] = __get_available_actions(command)
        result.append(module)

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


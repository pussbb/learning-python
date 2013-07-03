'''
Created on Jul 3, 2013

@author: pussbb
'''

from flask import Flask, abort
from werkzeug.exceptions import HTTPException
from api import json_responce
import traceback

import api.v01.app as app_v01

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

@app.errorhandler(Exception)
def exception_handler(exception=None):
    msg = ''
    code = 500

    if isinstance(exception, HTTPException):
        code = exception.code

    if app.config['DEBUG']:
        msg = traceback.format_exc()
    else:
        msg = str(exception)

    return json_responce({'error': msg}, code)

versions = [app_v01]

for v in versions:
    app.register_blueprint(v.api, url_prefix='/v.{0}'.format(v.VERSION)) 

@app.route('/')
def index():
    abort(404)


if __name__ == '__main__':
    app.run(port=5050)

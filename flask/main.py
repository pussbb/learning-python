'''
Created on Jul 3, 2013

@author: pussbb
'''

from flask import Flask, make_response, jsonify
from werkzeug.exceptions import HTTPException
import traceback

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

print app.config

def json_responce(data, code=200):
    return make_response(jsonify(data), code)

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

@app.route('/')
def index():
    raise Exception('spam', 'eggs')


if __name__ == '__main__':
    app.run(port=5050)


from flask import make_response, jsonify, Flask, abort, request
from werkzeug.exceptions import HTTPException

from flask_sqlalchemy import SQLAlchemy

import traceback

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)

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

@app.route('/api')
def index():
    abort(403)

def run_server():
    app.run(port=5050)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

from v01.app import api as api_v01
app.register_blueprint(api_v01)


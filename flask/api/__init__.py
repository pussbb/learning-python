
from flask import make_response, jsonify, Flask, abort, request
from werkzeug.exceptions import HTTPException

from flask_sqlalchemy import SQLAlchemy

import traceback

app = Flask(__name__)

if __debug__:
    app.config.from_object('api.config.DevelopmentConfig')
else:
    app.config.from_object('api.config.ProductionConfig')

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

@app.teardown_request
def apply_changes(exception=None):
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        exception_handler(e)
    finally:
        db.session.expunge_all()

def run_server():
    app.run(port=app.config['PORT'])

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/api')
def index():
    abort(403)

from v01.app import api as api_v01
app.register_blueprint(api_v01)


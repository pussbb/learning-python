
from flask import Flask, abort, request
from werkzeug.exceptions import HTTPException

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from output import output_response

import traceback

app = Flask(__name__)

if __debug__:
    app.config.from_object('api.config.DevelopmentConfig')
else:
    app.config.from_object('api.config.ProductionConfig')

db = SQLAlchemy(app)

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
    return output_response({'error': msg}, code)

@app.teardown_request
def apply_changes(exception=None):
    app.log_exception(exception)
    try:
        db.session.commit()
    except SQLAlchemyError as database_exception:
        db.session.rollback()
        exception_handler(database_exception)
    finally:
        db.session.remove()

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

from api.v01.app import api_v01
app.register_blueprint(api_v01)


'''
Init Flask application
@author: pussbb
'''

from flask import Flask, abort, request
from werkzeug.exceptions import HTTPException

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from api.output import output_response, output_error
from api.logger import attach_logger
from logging import getLogger
import traceback

app = Flask(__name__)

if __debug__:
    app.config.from_object('api.config.DevelopmentConfig')
else:
    app.config.from_object('api.config.ProductionConfig')

DB = SQLAlchemy(app)

attach_logger(app.logger, getLogger('sqlalchemy'), getLogger('DB'))

@app.errorhandler(Exception)
def exception_handler(exception=None):
    """Catch all exception and output them in requested format
    """
    msg = ''
    code = 500
    if isinstance(exception, HTTPException):
        code = exception.code
    if app.config['DEBUG']:
        msg = traceback.format_exc()
    else:
        msg = str(exception)
    return output_error(msg, code)

@app.teardown_request
def apply_changes(exception=None):
    """Commit all changes to database and remove scroped session
    """
    if exception:
        app.logger.exception(exception)
    try:
        DB.session.commit()
    except SQLAlchemyError as database_exception:
        DB.session.rollback()
        exception_handler(database_exception)
    finally:
        DB.session.remove()

def run_server():
    """Start application
    """
    app.run(port=app.config['PORT'])

def shutdown_server():
    """Shutdown server
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/api/')
def index():
    """Main route for application
    """
    abort(403)

from api.v01.app import API_V01
app.register_blueprint(API_V01)


'''
Init Flask application
@author: pussbb
'''

from flask import Flask, url_for, request
from werkzeug.exceptions import HTTPException

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from .output import output_response, output_error
from .logger import attach_logger
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

@app.route('/')
def index():
    """Main route for application
    """
    data = {}
    for i, v in app.blueprints.items():
        data[i] = url_for("{0}.index".format(v.name), _external=True)
    return output_response(data)

from .v01.app import API_V01

app.register_blueprint(API_V01)

'''
class Dispatcher(object):
    def __init__(self, app):
        self.app = app
        self.wsgi_app = app.wsgi_app

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

app.wsgi_app = Dispatcher(app)

'''

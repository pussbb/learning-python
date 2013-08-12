'''
Created on Jul 3, 2013

@author: pussbb
'''

class Config(object):
    PORT = 5050
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/speeddial'
    TRAP_HTTP_EXCEPTIONS = True
    TRAP_BAD_REQUEST_ERRORS = False
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = False

class ProductionConfig(Config): pass

class DevelopmentConfig(Config):
    DEBUG = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    TRAP_BAD_REQUEST_ERRORS = True

class TestingConfig(Config):
    TESTING = True
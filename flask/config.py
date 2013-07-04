'''
Created on Jul 3, 2013

@author: pussbb
'''

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/speeddial'
    TRAP_HTTP_EXCEPTIONS = True
    TRAP_BAD_REQUEST_ERRORS = True
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = False

class ProductionConfig(Config): pass

class DevelopmentConfig(Config):
    DEBUG = True
    JSONIFY_PRETTYPRINT_REGULAR = True

class TestingConfig(Config):
    TESTING = True
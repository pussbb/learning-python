'''
Created on Jul 3, 2013

@author: pussbb
'''


class Config(object):
    PORT = 5050
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@localhost/speeddial'
    TRAP_HTTP_EXCEPTIONS = True
    TRAP_BAD_REQUEST_ERRORS = False
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    LOG_FILENAME = 'log/access.log'
    LOG_MAX_BYTES = 524288000
    LOG_BACKUP_COUNT = 5
    SQLALCHEMY_RECORD_QUERIES = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    TRAP_BAD_REQUEST_ERRORS = True


class TestingConfig(Config):
    TESTING = True

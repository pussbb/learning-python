'''
Created on Jul 3, 2013

@author: pussbb
'''

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
    TRAP_HTTP_EXCEPTIONS = True

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://root@localhost/speeddial'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
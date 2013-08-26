'''
Created on Aug 26, 2013

@author: pussbb
'''

import logging
import logging.handlers

import api.config
import os

__all__ = (
    'LOGGER',
    'attach_logger',
)

config = api.config.Config

if __debug__:
    config = api.config.DevelopmentConfig
else:
    config = api.config.ProductionConfig

path = os.path.abspath(os.path.dirname(config.LOG_FILENAME))
if not os.path.exists(path) or not os.path.isdir(path):
    os.mkdir(path)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

log_handler = logging.handlers.RotatingFileHandler(
     config.LOG_FILENAME,
     maxBytes= config.LOG_MAX_BYTES, 
     backupCount= config.LOG_BACKUP_COUNT
)

_formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")

LOGGER.addHandler(log_handler)

def attach_logger(*args):
    for logger in args:
        logger.propagate = False
        del logger.handlers[:]
        logger.addHandler(log_handler)

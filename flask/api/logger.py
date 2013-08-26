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

CONFIG = api.config.Config

if __debug__:
    CONFIG = api.config.DevelopmentConfig
else:
    CONFIG = api.config.ProductionConfig

path = os.path.abspath(os.path.dirname(CONFIG.LOG_FILENAME))
if not os.path.exists(path) or not os.path.isdir(path):
    os.mkdir(path)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(
     CONFIG.LOG_FILENAME,
     maxBytes= CONFIG.LOG_MAX_BYTES,
     backupCount= CONFIG.LOG_BACKUP_COUNT
)

logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")

LOGGER.addHandler(handler)

def attach_logger(*args):
    for logger in args:
        logger.propagate = False
        del logger.handlers[:]
        logger.addHandler(handler)

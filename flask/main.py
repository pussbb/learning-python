'''
Created on Jul 3, 2013

@author: pussbb
'''
from __future__ import absolute_import, unicode_literals


import logging.config


from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

logging.config.fileConfig("logger.cfg", disable_existing_loggers=False)

import api
import blog



application = DispatcherMiddleware(blog.app, {
    '/api': api.app
})


if __name__ == '__main__':
    # run api server
    run_simple('0.0.0.0', 5050, application, use_reloader=True)
    #api.run_server()
    #blog.run_server()


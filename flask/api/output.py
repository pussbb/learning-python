'''
Created on Aug 25, 2013

@author: pussbb
'''

__all__ = (
    'REPRESENTATIONS',
    'output_response',
    'output_error',
)

from flask import make_response, jsonify, request
from simplexml import dumps

def json_response(data, code=200):
    ''' Return Response object wich containce JSON
    '''
    resp = make_response(jsonify(data), code)
    resp.headers['Content-Type'] = 'application/json'
    return resp


def xml_response(data, code=200):
    ''' Return Response object wich containce XML
    '''
    resp = make_response(dumps({'response': data}), code)
    resp.headers['Content-Type'] = 'application/xml'
    return resp

REPRESENTATIONS = {
                   'application/json': json_response,
                   'application/xml': xml_response
                   }

def output_response(data, code=200, mediatype=None):
    '''Return proper Response object in requested format.
    By default format will get from HTTP request attrinbute 'Accept'
    if does not support mediatype JSON string will be returned.
    '''
    if not mediatype:
        mediatype = request.headers.get('accept')
    func = json_response
    if mediatype in REPRESENTATIONS:
        func = REPRESENTATIONS[mediatype]
    return func(data, code)


def output_error(data, code=400):
    '''Helper function to unify output errors format
    '''
    return output_response({'errors': data}, code)


'''
Created on Aug 25, 2013
>>> from requests import get
>>> get('http://localhost:5000/me').content # default_mediatype
'<?xml version="1.0" ?><response><hello>me</hello></response>'
>>> get('http://localhost:5000/me', headers={"accept":"application/json"}).content
'{"hello": "me"}'
>>> get('http://localhost:5000/me', headers={"accept":"application/xml"}).content
'<?xml version="1.0" ?><response><hello>me</hello></response>'

@author: pussbb
'''

__all__ = (
    'REPRESENTATIONS',
    'output_response',
)


# needs: pip install python-simplexml
from flask import make_response, jsonify, request
from simplexml import dumps
# you need requests



def json_response(data, code=200):
    resp = make_response(jsonify(data), code)
    resp.headers['Content-Type'] = 'application/json'
    return resp

def xml_response(data, code=200):
    resp = make_response(dumps({'response' :data}), code)
    resp.headers['Content-Type'] = 'application/xml'
    return resp

REPRESENTATIONS = {
                   'application/json': json_response,
                   'application/xml': xml_response
                   }

def output_response(data, code=200, mediatype=None):

    if not mediatype:
        mediatype = request.headers.get('accept')
    func = json_response
    if mediatype in REPRESENTATIONS:
        func = REPRESENTATIONS[mediatype]
    return func(data, code)


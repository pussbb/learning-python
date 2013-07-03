
from flask import make_response, jsonify

def json_responce(data, code=200):
    return make_response(jsonify(data), code)

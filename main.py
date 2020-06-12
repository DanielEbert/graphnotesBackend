#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, request, current_app
from flask_cors import CORS
from json import dumps

import utils
import db as database


db = database.DB()

app = Flask(__name__)
CORS(app)


@app.route("/loadState", methods=['POST'])
def loadState():
    user = authorizedUser(request.headers)
    if user is None:
        return "F", 401
    ret = db.load(user)
    if ret[0] is False or not ret[1]:
        return jsonify({})
    return ret[1][0]

@app.route("/saveState", methods=['POST'])
def saveState():
    user = authorizedUser(request.headers)
    if user is None:
        return "F", 401
    data = dumps(request.get_json())
    print(user, data)
    db.save(user, data)
    return ""

def authorizedUser(requestHeaders) -> str:
    if not 'Authorization' in requestHeaders:
        return None
    headerAuth = requestHeaders['Authorization'].split()
    if len(headerAuth) != 2:
        return None
    if headerAuth[0] != "Bearer":
        return None
    r = utils.authAccessToken(headerAuth[1])
    if r[0] is False:
        return None
    return r[1]

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=False)

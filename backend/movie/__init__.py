from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
from json import dumps
import redis


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
CORS(app)
app.register_error_handler(Exception, defaultHandler)
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
# next line is for multi env
# app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
Session(app)

from movie import controllers
from movie import models
from movie import error

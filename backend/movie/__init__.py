from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
from json import dumps
import redis
import smtplib
from email.mime.text import MIMEText
from config import EMAIL, SMTP_SERVER, MAIL_PASS

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
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
# next line is for multi env
# app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
db.pool_pre_ping=True
Session(app)

# smtp
smptyserver = smtplib.SMTP(SMTP_SERVER)
smptyserver.login(EMAIL, MAIL_PASS)


from movie import controllers
from movie import models
from movie import error
from movie.controllers import auth_bp, admin_bp, event_bp, movie_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(event_bp)
app.register_blueprint(movie_bp)

db.create_all()
db.session.commit()

#TODO: remember to remove the comment(#)
#app.register_error_handler(Exception, defaultHandler)
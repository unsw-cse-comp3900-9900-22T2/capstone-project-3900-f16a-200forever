from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
from json import dumps
import redis
import smtplib
from email.mime.text import MIMEText
from config import EMAIL, SMTP_SERVER, MAIL_PASS
from redis import Redis

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = {
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    }
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

# redis
redis_pool= redis.ConnectionPool(host="127.0.0.1", port= 6379, db= 0)
redis_cli = redis.Redis(connection_pool= redis_pool)
print(redis_cli)


from movie import controllers
from movie import models
from movie import error
from movie.controllers import auth_bp, event_bp, movie_bp, person_bp, user_bp, genre_bp, review_bp, recommendation_bp, thread_bp

app.register_blueprint(auth_bp)
app.register_blueprint(event_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(person_bp)
app.register_blueprint(user_bp)
app.register_blueprint(genre_bp)
app.register_blueprint(review_bp)
app.register_blueprint(recommendation_bp)
app.register_blueprint(thread_bp)

db.create_all()
db.session.commit()

#TODO: remember to remove the comment(#)
#app.register_error_handler(Exception, defaultHandler)
from enum import unique
from hashlib import algorithms_available
import re
from sqlalchemy import *
from movie import db
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base



class Users(db.Model):
  __tablename__ = 't_users'
  id = db.Column('id', db.String(256), primary_key=True)
  name = db.Column('name', db.String(256), nullable=False)
  email = db.Column('email', db.String(256), unique=True, nullable=False)
  # public_status = db.Column('public_status', db.Boolean)
  signature = db.Column('signature', db.String)
  image = db.Column('image', db.BLOB)
  password = db.Column('password', db.String, nullable=False)
  validation_code = db.Column('validation_code', db.String)
  code_expriy_time = db.Column('code_expriy_time', db.DateTime)
  events = db.relationship('Events', secondary='r_user_event', back_populates='users', lazy=True)
  
  def __repr__(self):
    return '<User {} {}>'.format(self.name, self.email)

  def __init__(self, data):
    self.id = data['id']
    self.name = data['name']
    self.email = data['email']
    self.password = data['password']
    
  """
    @email.setter
  def email(self, new_email):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(pattern, new_email):
      self.__email = new_email
    else:
      # TODO:
      #raise error
      pass
  """

      
class UserEvent(db.Model):
  __tablename__ = 'r_user_event'
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), nullable=False, primary_key=True)
  event_id = db.Column('event_id', db.String(256), db.ForeignKey('t_events.id'), nullable=False, primary_key=True)

  def __repr__(self):
    return '<UserEvent user id:{} event id:{}>'.format(self.user_id, self.event_id)

  def __init__(self, data):
    self.user_id = data['user_id']
    self.event_id = data['event_id']


class WishlistMovie(db.Model):
  __tablename__ = 'r_wishlist_movie'
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), nullable=False, primary_key=True)
  movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('t_movies.id'), primary_key=True)

  def __repr__(self):
    return '<WishlistMovie user id:{} movie id:{}>'.format(self.user_id, self.movie_id)

  def __init__(self, data):
    self.user_id = data['user_id']
    self.movie_id = data['movie_id']


class WatchedlistMovie(db.Model):
  __tablename__ = 'r_WatchedList_movie'
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), nullable=False, primary_key=True)
  movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('t_movies.id'), primary_key=True)

  def __repr__(self):
    return '<WatchedListMovie user id:{} movie id:{}>'.format(self.user_id, self.movie_id)

  def __init__(self, data):
    self.user_id = data['user_id']
    self.movie_id = data['movie_id']


class DroppedlistMovie(db.Model):
  __tablename__ = 'r_DroppedList_movie'
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), nullable=False, primary_key=True)
  movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('t_movies.id'), primary_key=True)

  def __repr__(self):
    return '<DroppedListMovie user id:{} movie id:{}>'.format(self.user_id, self.movie_id)

  def __init__(self, data):
    self.user_id = data['user_id']
    self.movie_id = data['movie_id']
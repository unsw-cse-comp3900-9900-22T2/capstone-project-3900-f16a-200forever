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
  #public_status = db.Column('public_status', db.Boolean)
  signature = db.Column('signature', db.String(256))
  image = db.Column('image', db.String(256))
  password = db.Column('password', db.String(256), nullable=False)
  validation_code = db.Column('validation_code', db.String(256))
  code_expriy_time = db.Column('code_expriy_time', db.DateTime)
  # relationships from reviews
  #reviews = db.relationship('Reviews', backref='users', lazy=True)
  #review_likes = db.relationship('ReviewLikes', backref='users', lazy=True)
  #review_unlikes = db.relationship('ReviewUnlikes', backref='users', lazy=True)
  user_review_likes_rel = db.relationship(
      "Reviews",
      secondary='r_review_likes',
      back_populates="review_user_likes_rel",
      lazy=True,
      overlaps="user_review_unlikes_rel"
  )
  user_review_unlikes_rel = db.relationship(
      "Reviews",
      secondary='r_review_unlikes',
      back_populates="review_user_unlikes_rel",
      lazy=True,
      overlaps="user_review_likes_rel"
  )
  events =  db.relationship('Events', secondary='r_user_event', back_populates='users', lazy=True)
  
  def __repr__(self):
    return '<User {} {}>'.format(self.name, self.email)

  def __init__(self, data):
    self.id = data['id']
    self.name = data['name']
    self.email = data['email']
    self.password = data['password']
    

class UserEevnt(db.Model):
  __tablename__ = 'r_user_event'
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), primary_key=True, nullable=False)
  event_id = db.Column('event_id', db.String(256), db.ForeignKey('t_events.id'), primary_key=True, nullable=False)
  event_status = db.Column('event_status', db.String(256), nullable=False)
  start_time = db.Column('start_time', db.DateTime, nullable=False)
  end_time = db.Column('end_time', db.DateTime)

  def __repr__(self):
    return '<UserEvent user id: {} event id: {}>'.format(self.user_id, self.event_id)

  def __init__(self, data):
    self.user_id = data['user_id']
    self.event_id = data['event_id']
    self.event_status = 'attemping'
    self.start_time = data['start_time']
 
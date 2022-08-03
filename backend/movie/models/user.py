from enum import unique
from hashlib import algorithms_available
import re
from sqlalchemy import *
from movie import db
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy.orm import backref
from datetime import datetime

#--------------------USER-------------------
class Users(db.Model):
  __tablename__ = 't_users'
  id = db.Column('id', db.String(256), primary_key=True)
  name = db.Column('name', db.String(256), nullable=False)
  email = db.Column('email', db.String(256), unique=True, nullable=False)
  signature = db.Column('signature', db.String(256))
  image = db.Column('image', db.String(256))
  password = db.Column('password', db.String(256), nullable=False)
  validation_code = db.Column('validation_code', db.String(256))
  code_expriy_time = db.Column('code_expriy_time', db.DateTime)
  is_forum_admin = db.Column('is_forum_admin', db.Integer, nullable=False)
  is_review_admin = db.Column('is_review_admin', db.Integer, nullable=False)
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

  user_watched_list = db.relationship(
    "Movies", 
    secondary='r_watchedlist_movie', 
    backref='watched_list_users',
    lazy=True,
    overlaps = "user_dropped_list, user_wish_list"
  )

  user_dropped_list = db.relationship(
    "Movies", 
    secondary='r_droppedlist_movie', 
    backref='dropped_list_users',
    lazy=True,
    overlaps = "user_watched_list, user_wish_list"
  )

  user_wish_list = db.relationship(
    "Movies", 
    secondary='r_wishlist_movie', 
    backref='wish_list_users',
    lazy=True,
    overlaps = "user_watched_list, user_dropped_list"
  )
  events =  db.relationship('Events', secondary='r_user_event', back_populates='users', lazy=True)
  threads = db.relationship('Threads', backref='user', lazy=True)
  reviews = db.relationship('Reviews', backref='user', lazy=True)
  thread_comments = db.relationship('ThreadComment', backref='user', lazy=True)
  user_follow_list = db.relationship('FollowList', foreign_keys="FollowList.user_id", backref='follow_own', lazy=True)
  user_follower_list = db.relationship('FollowList', foreign_keys="FollowList.follow_id", backref='follower', lazy=True)
  user_banned_list = db.relationship('BannedList', foreign_keys="BannedList.user_id", backref='banned_own', lazy=True)
  user_be_banned_list = db.relationship('BannedList',foreign_keys="BannedList.banned_user_id",  backref='banner', lazy=True)
  comment_likes = db.relationship('ThreadLikes', backref='user', lazy=True)

  def __repr__(self):
    return '<User {} {}>'.format(self.name, self.email)

  def __init__(self, data):
    self.id = data['id']
    self.name = data['name']
    self.email = data['email']
    self.password = data['password']
    self.is_forum_admin = 0
    
#--------------------USER EVENT-------------------
class UserEvent(db.Model):
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
 
#--------------------FOLLOW LIST & BANNED LIST--------------------
class FollowList(db.Model):
  __tablename__ = 'r_follow_list'
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), primary_key=True, nullable=False)
  follow_id = db.Column('follow_id', db.String(256), db.ForeignKey('t_users.id'), primary_key=True, nullable=False)

  def __repr__(self):
    return '<FollowList user id: {} follow id: {}>'.format(self.user_id, self.follow_id)
  
  def __init__(self, data):
    self.user_id = data['user_id']
    self.follow_id = data['follow_id']

class BannedList(db.Model):
  __tablename__ = 'r_banned_list'
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), primary_key=True, nullable=False)
  banned_user_id = db.Column('banned_user_id', db.String(256), db.ForeignKey('t_users.id'), primary_key=True, nullable=False)

  def __repr__(self):
    return '<BannedList user id: {} banned id: {}>'.format(self.user_id, self.banned_user_id)
  
  def __init__(self, data):
    self.user_id = data['user_id']
    self.banned_user_id = data['banned_user_id']


#--------------------MOVIE LIST--------------------
class MovieDroppedList(db.Model):
  __tablename__ = 'r_droppedlist_movie'
  movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('t_movies.id'), primary_key=True, nullable=False)
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), primary_key=True, nullable=False)
  added_time = db.Column('added_time', db.String(256), nullable=False)

  def __repr__(self):
    return '<DroppedList user id: {} movie id: {}>'.format(self.user_id, self.movie_id)
  
  def __init__(self, data):
    self.user_id = data['user_id']
    self.movie_id = data['movie_id']
    self.added_time = str(datetime.now())

class MovieWatchedList(db.Model):
  __tablename__ = 'r_watchedlist_movie'
  movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('t_movies.id'), primary_key=True, nullable=False)
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), primary_key=True, nullable=False)
  added_time = db.Column('added_time', db.String(256), nullable=False)

  def __repr__(self):
    return '<WatchedList user id: {} movie id: {}>'.format(self.user_id, self.movie_id)
  
  def __init__(self, data):
    self.user_id = data['user_id']
    self.movie_id = data['movie_id']
    self.added_time = str(datetime.now())
    

class MovieWishList(db.Model):
  __tablename__ = 'r_wishlist_movie'
  movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('t_movies.id'), primary_key=True, nullable=False)
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), primary_key=True, nullable=False)
  added_time = db.Column('added_time', db.String(256), nullable=False)

  def __repr__(self):
    return '<WishList user id: {} movie id: {}>'.format(self.user_id, self.movie_id)
  
  def __init__(self, data):
    self.user_id = data['user_id']
    self.movie_id = data['movie_id']
    self.added_time = str(datetime.now())

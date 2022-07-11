from unicodedata import category
from xml.etree.ElementTree import Comment
from movie import db

class Threads(db.Model):
  __tablename__ = 't_threads'
  id = db.Column('id', db.String(256), primary_key=True)
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), nullable=False)
  category_id = db.Column('category_id', db.String(256), nullable=False)
  created_time = db.Column('created_time', db.DateTime, nullable=False)
  is_anonymous = db.Column('is_anonymous', db.Integer, nullable=False)
  title = db.Column('title', db.String(100), nullable=False)
  content = db.Column('content', db.String(10000), nullable=False)
  comments = db.relationship("ThreadComment", back_populates="thread", lazy=True)
  

  def __repr__(self):
    return '<Thread: id{} user_id{}>'.format(self.id, self.user_id)
  
  def __init__(self, data):
    if data['is_anonymous'] != 1 or data['is_anonymous'] != 0:
      raise
    self.id = data['id']
    self.user_id = data['user_id']
    self.category_id = data['category_id']
    self.created_time = data['created_time']
    self.title = data['title']
    self.is_anonymous = data['is_anonymous']
    self.content = data['content']

class Categories(db.Model):
  __tablename__ = 't_categories'
  id = db.Column('id', db.String(256), primary_key=True)
  #genre_id = db.Column('genre_id', db.Integer, db.ForeignKey('t_genres.id'), nullable=False)
  name = db.Column('name', db.String(256), nullable=False)

  def __repr__(self):
    return '<Category: id{} name{}>'.format(self.id, self.name)
  
  def __init__(self, data):
    self.id = data['id']
    self.genre_id = data['genre_id']
    self.name = data['name']

class ThreadComment(db.Model):
  __tablename__ ='t_thread_comment'
  id = db.Column('id', db.String(256), primary_key=True)
  thread_id = db.Column('thread_id', db.Integer, db.ForeignKey('t_threads.id'), nullable=False)
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), nullable=False)
  reply_comment_id = db.Column('reply_comment_id', db.String(256), db.ForeignKey('t_thread_comment.id'),  nullable=False)
  comment_time = db.Column('comment_time', db.DateTime, nullable=False)
  content = db.Column('content', db.String(256), nullable=False)
  is_anonymous = db.Column('is_anonymous', db.Integer, nullable=False)  
  comments = db.relationship("ThreadComment", back_populates="comments", lazy=True)


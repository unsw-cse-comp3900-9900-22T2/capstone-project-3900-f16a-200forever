from re import S
from xml.etree.ElementTree import Comment
from movie import db

class Threads(db.Model):
  __tablename__ = 't_threads'
  id = db.Column('id', db.String(256), primary_key=True)
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), nullable=False)
  genre_id = db.Column('genre_id', db.String(256), db.ForeignKey('t_genres.id'), nullable=False)
  created_time = db.Column('created_time', db.String(256), nullable=False)
  is_anonymous = db.Column('is_anonymous', db.Integer, nullable=False)
  title = db.Column('title', db.String(100), nullable=False)
  content = db.Column('content', db.String(10000), nullable=False)
  comments = db.relationship("ThreadComment", backref="thread", lazy=True)
  thread_likes = db.relationship("ThreadLikes", backref="thread", lazy=True)
  
  def __repr__(self):
    return '<Thread: id{} user_id{}>'.format(self.id, self.user_id)
  
  def __init__(self, data):
    if data['is_anonymous'] != 1 and data['is_anonymous'] != 0:
      raise
    self.id = data['id']
    self.user_id = data['user_id']
    self.genre_id = data['genre_id']
    self.created_time = data['created_time']
    self.title = data['title']
    self.is_anonymous = data['is_anonymous']
    self.content = data['content']


class ThreadComment(db.Model):
  __tablename__ ='t_thread_comment'
  id = db.Column('id', db.String(256), primary_key=True)
  thread_id = db.Column('thread_id', db.String(256), db.ForeignKey('t_threads.id'), nullable=False)
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), nullable=False)
  reply_comment_id = db.Column('reply_comment_id', db.String(256), db.ForeignKey('t_thread_comment.id'))
  comment_time = db.Column('comment_time', db.String(256), nullable=False)
  content = db.Column('content', db.String(256), nullable=False)
  is_anonymous = db.Column('is_anonymous', db.Integer, nullable=False)  
  comments = db.relationship("ThreadComment", remote_side=[id])

  def __repr__(self):
    return '<Comment: user_id{} comment_id{}>'.format(self.user_id, self.thread_id)

  def __init__(self, data):
    self.id = data['id']
    self.user_id = data['user_id']
    self.thread_id = data['thread_id']
    if 'reply_comment_id' in data.keys():
      self.reply_comment_id = data['reply_comment_id']
    else:
      self.reply_comment_id = None
    self.comment_time = data['time']
    self.content = data['content']
    self.is_anonymous = data['is_anonymous']


class ThreadLikes(db.Model):
  __tablename__ = 'r_thread_likes'
  user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), nullable=False, primary_key = True)
  thread_id = db.Column('thread_id', db.String(256), db.ForeignKey('t_threads.id'), nullable=False, primary_key = True)

  def __repr__(self):
    return '<ThreadLikes: user_id{} thread_id{}>'.format(self.user_id, self.thread_id)

  def __init__(self, data):
    self.user_id = data['user_id']
    self.thread_id = data['thread_id']



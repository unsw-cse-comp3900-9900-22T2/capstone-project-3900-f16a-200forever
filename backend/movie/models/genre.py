from movie import db
from sqlalchemy import *

class Genres(db.Model):
  __tablename__ = 't_genres'
  id = db.Column('id', db.String(256), primary_key=True)
  name = db.Column('name', db.String(256), nullable=False)
  genre_movie = db.relationship('Movies', secondary='r_movie_genre', back_populates='movie_genre', lazy=True)
  threads = db.relationship('Threads', backref="genre", lazy=True)
  
  def __repr__(self):
    return '<Genre id:{} name:{}>'.format(self.id, self.name)
  
  def __init__(self, id, name):
    self.id = id
    self.name = name


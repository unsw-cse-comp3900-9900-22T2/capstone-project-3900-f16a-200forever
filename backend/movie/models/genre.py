from movie import db
from sqlalchemy import *

class Genres(db.Model):
  __tablename__ = 't_genres'
  id = db.Column('id', db.String(32), primary_key=True)
  name = db.Column('name', db.String(256), nullable=False)
  genre_movie = db.relationship('Movies', secondary='r_movie_genre', back_populates='movie_genre', lazy=True)

  def __repr__(self):
    return '<Genre id:{} name:{}>'.format(self.id, self.name)
  
  def __init__(self, id, name):
    self.id = id
    self.name = name

class MovieGenre(db.Model):
  __tablename__ = 'r_movie_genre'
  genre_id = db.Column('genre_id', db.Integer, db.ForeignKey('t_genres.id'), primary_key=True)
  movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('t_movies.id'), primary_key=True)

  def __repr__(self):
    return '<MovieGenre movie id: {} genren id: {}>'.format(self.movie_id, self.genre_id)

  def __init__(self, data):
    self.genre_id = data['genre_id']
    self.movie_id = data['movie_id']
from movie import db
from sqlalchemy import *
from movie.models.genre import Genres
from movie.models.review import Reviews

class Movies(db.Model):
  __tablename__ = 't_movies'
  id = db.Column('id', db.Integer, primary_key=True)
  title = db.Column('title' ,db.String(200), nullable=False)
  tagline = db.Column('tagline', db.String(200))
  backdrop = db.Column('backdrop', db.String(200))
  description = db.Column('description', db.String(1000))
  runtime = db.Column('runtime', db.Integer)
  release_time = db.Column('release_time', db.String(256))
  release_status = db.Column('release_status', db.String(20))
  total_rating = db.Column('total_rating', db.Float(20))
  rating_count = db.Column('rating_count', db.Integer)
  events = db.relationship('Events', secondary='r_event_movie', back_populates='movies', lazy=True)
  #movie_director_rel = db.relationship('Persons', secondary='r_movie_director', back_populates='person_movie_rel', lazy=True)
  #movie_actor_rel = db.relationship('Persons', secondary='r_movie_actor', back_populates='actor_movie_rel', lazy=True)
  movie_genre = db.relationship('Genres', secondary='r_movie_genre', back_populates='genre_movie', lazy=True)
  images = db.relationship('MovieImages', backref='movie', lazy=True)
  movie_director_rel = db.relationship(
        "Persons",
        secondary='r_movie_director', 
        back_populates="director_movie_rel",
        lazy=True,
        #overlaps="movie_actor_rel, director_movie_rel"
        overlaps="movie_actor_rel"
  )
  movie_actor_rel = db.relationship(
        "Persons",
        secondary='r_movie_actor',
        back_populates="director_movie_rel",
        #overlaps="movie_director_rel, actot_movie_rel"
        overlaps="movie_director_rel"
  )

  # relationships from reviews
  reviews = db.relationship('Reviews', backref='movies', lazy=True)

  def __repr__(self):
    return '<Movie: {} {}>'.format(self.id, self.title)

  def __init__(self, data):
    self.id = data['id']
    self.title = data['title']
    self.tagline = data['tagline']
    self.backdrop = data['backdrop']
    self.discription = data['discription']
    self.runtime = data['runtime']
    self.release_date = data['release_date']
    self.release_status = data['release_status']
    self.total_rating = data['total_rating']
    self.rating_count = data['rating_count']

class MovieImages(db.Model):
  __tablename__ = 't_movie_images'
  id = db.Column('id', db.Integer, primary_key=True)
  file_path = db.Column('file_path', db.String(256), nullable=False)
  height = db.Column('height', db.Integer)
  width = db.Column('width', db.Integer)
  movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('t_movies.id'))

  def __repr__(self):
    return '<Images id: {} movie id : {}>'.format(self.id, self.movie_id)

  def __init__(self, data):
    self.id = data['id']
    self.movie_id = data['movie_id']
    self.file_path = data['file_path']
    self.height = data['height']
    self.width = data['width']

class MovieGenre(db.Model):
  __tablename__ = 'r_movie_genre'
  genre_id = db.Column('genre_id', db.Integer, db.ForeignKey('t_genres.id'), primary_key=True)
  movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('t_movies.id'), primary_key=True)

  def __repr__(self):
    return '<MovieGenre movie id: {} genren id: {}>'.format(self.movie_id, self.genre_id)

  def __init__(self, data):
    self.genre_id = data['genre_id']
    self.movie_id = data['movie_id']
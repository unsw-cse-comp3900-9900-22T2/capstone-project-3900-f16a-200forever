from movie import db
from sqlalchemy import *

class Persons(db.Model):
  __tablename__ = 't_persons'
  id = db.Column('id', db.Integer, primary_key=True)
  title = db.Column('title', db.String(256), nullable=False)
  tagline = db.Column('tagline', db.String(256))
  backdrop = db.Column('backdrop', db.String(256))
  discription = db.Column('discription', db.String(256))
  runtime = db.Column('runtime', db.Integer)
  release_time = db.Column('release_time', db.DateTime)
  release_status = db.Column('release_status', db.String(256))
  director_movie_rel = db.relationship('Movies', secondary='r_movie_director', back_populates='movie_director_rel', lazy=True)
  actor_movie_rel = db.relationship('Movies', secondary='r_movie_actor', back_populates='movie_actor_rel', lazy=True)

  def __repr__(self):
    return '<Movie id:{} title :{}>'.format(self.id, self.title)

  def __init__(self, id):
    self.id = id

class MovieDirector(db.Model):
    __tablename__ = 'r_movie_director'
    movie_id = db.Column('movie_id', db.Integer(20), db.ForeignKey('Movies.id'))
    person_id = db.Column('person_id', db.Integer(20), db.ForeignKey('Persons.id'))

    def __repr__(self):
      return '<Movie id: {} director id: {}>'.format(self.movie_id, self.person_id)

    def __init__(self, data):
      self.movie_id = data['movie_id']
      self.person_id = data['person_id']
      

class MovieActor(db.Model):
    __tablename__ = 'r_movie_actor'
    movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('t_movies.id'), primary_key=True)
    person_id = db.Column('person_id', db.Integer, db.ForeignKey('t_persons.id'), primary_key=True)
    character = db.Column('character', db.String(256), nullable=False)
    order = db.Column('order', db.Integer, nullable=False)

    def __repr__(self):
      return '<ActorMovie movie id: {} actor id: {} character: {}>'.format(self.movie_id, self.actor_id, self.character)

    def __init__(self, data):
      self.movie_id = data['movie_id']
      self.person_id = data['person_id']
      self.character = data['character']
      self.order = data['order']



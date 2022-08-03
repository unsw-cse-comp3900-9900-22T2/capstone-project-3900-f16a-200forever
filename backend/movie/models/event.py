#from locale import T_FMT
from sqlalchemy import true
from movie import db
from movie.models.movie import Movies

class Events(db.Model):
  __tablename__ = 't_events'
  id = db.Column('id', db.String(256), primary_key=True)
  event_status = db.Column('event_status', db.String(256))
  topic = db.Column('topic', db.String(256))
  duration = db.Column('duration', db.Integer)
  deadline = db.Column('deadline', db.DateTime)
  image_description = db.Column('image_description', db.String(256))
  image = db.Column('image', db.BLOB)
  description = db.Column('description', db.String(256))
  require_correctness_amt = db.Column('require_correctness_amt', db.Integer)
  admin_id = db.Column(db.Integer, db.ForeignKey('t_admins.id'), nullable=False)
  questions = db.relationship('Questions', back_populates="event", lazy=True)
  movies = db.relationship('Movies', secondary='r_event_movie', back_populates='events', lazy=True)
  users = db.relationship('Users', secondary='r_user_event', back_populates='events', lazy=True)
  
  def __repr__(self):
    return '<Event id:{} admin id:{}>'.format(self.id, self.admin_id)
  
  def __init__(self, data):
    self.id = data['id']
    self.topic = data['topic']
    self.duration = data['duration']
    self.deadline = data['deadline']
    self.image_description = data['image_description']
    self.description = data['description']
    self.require_correctness_amt = data['require_correctness_amt']
    self.admin_id = data['admin_id']

class Questions(db.Model):
  __tablename__ = 't_questions'
  id = db.Column('id', db.String(256), primary_key=True)
  content = db.Column('content', db.String(256), nullable=False)
  choice_1 = db.Column('choice_1', db.String(256), nullable=False)
  choice_2 = db.Column('choice_2', db.String(256), nullable=False)
  choice_3 = db.Column('choice_3', db.String(256), nullable=False)
  correct_answer = db.Column('correct_answer', db.Integer, nullable=False)
  db.CheckConstraint('correct_answer>=1 and correct_answer<=3', name='check_correct_answer')
  event = db.relationship("Events", back_populates="questions", lazy=True)
  event_id = db.Column('event_id', db.String(256), db.ForeignKey('t_events.id'), nullable=False)

  def __repr__(self):
    return '<Question id:{} event id:{}>'.format(self.id, self.event_id)
  
  def __init__(self, data):
    self.id = data['id']
    self.content = data['content']
    self.choice_1 = data['choice_1']
    self.choice_2 = data['choice_2']
    self.choice_3 = data['choice_3']
    self.correct_answer = data['correct_answer']
    self.event_id = data['event_id']

class EventMovie(db.Model):
  __tablename__ = 'r_event_movie'
  movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('t_movies.id'), nullable=False, primary_key=True)
  event_id = db.Column('event_id', db.String(256), db.ForeignKey('t_events.id'), nullable=False, primary_key=True)

  def __repr__(self):
    return '<EventMovie movie id:{} event id:{}>'.format(self.movie_id, self.event_id)

  def __init__(self, data):
    self.movie_id = data['movie_id']
    self.event_id = data['event_id']



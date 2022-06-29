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

  def __repr__(self):
    return '<Movie id:{} title :{}>'.format(self.id, self.title)

  def __init__(self, id):
    self.id = id

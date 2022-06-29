from movie import db
from sqlalchemy import *

class Genres(db.Model):
  __tablename__ = 't_genres'
  id = db.Column('id', db.String(32), primary_key=True)
  name = db.Column('name', db.String(256), nullable=False)

  def __repr__(self):
    return '<Genre id:{} name:{}>'.format(self.id, self.name)
  
  def __init__(self, id, name):
    self.id = id
    self.name = name
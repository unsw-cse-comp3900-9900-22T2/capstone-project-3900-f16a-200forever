from multiprocessing import parent_process
from movie import db

class Admins(db.Model):
  __tablename__ = 't_admins'
  id = db.Column('id', db.Integer, primary_key=True)
  email = db.Column('email', db.String(256), unique=True, nullable=False)
  password = db.Column('password', db.String(256), nullable=False)
  events = db.relationship('Events', backref='admin', lazy=True)

  def __repr__(self):
    return '<Admin {} {}>'.format(self.id, self.email)
  
  def __init__(self, email, password):
    self.email = email
    self.password = password

from enum import unique
from hashlib import algorithms_available
import re
from sqlalchemy import *
from movie import db
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base



class Users(db.Model):
  __tablename__ = 't_users'
  id = db.Column('id', db.String(256), primary_key=True)
  name = db.Column('name', db.String(256), nullable=False)
  email = db.Column('email', db.String(256), unique=True, nullable=False)
  #public_status = db.Column('public_status', db.Boolean)
  signature = db.Column('signature', db.String)
  image = db.Column('image', db.String)
  password = db.Column('password', db.String, nullable=False)
  validation_code = db.Column('validation_code', db.String)
  code_expriy_time = db.Column('code_expriy_time', db.DateTime)
  
  def __repr__(self):
    return '<User {} {}>'.format(self.name, self.email)

  def __init__(self, data):
    self.id = data['id']
    self.name = data['name']
    self.email = data['email']
    self.password = data['password']
    
  """
    @email.setter
  def email(self, new_email):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(pattern, new_email):
      self.__email = new_email
    else:
      # TODO:
      #raise error
      pass
  """

      

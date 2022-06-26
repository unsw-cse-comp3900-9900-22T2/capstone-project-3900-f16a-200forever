from movie import db

class Admins(db.Model):
  __tablename__ = 't_admins'
  id = db.Column('id', db.Integer, primary_key=True)
  email = db.Column('email', db.String(256), unique=True, nullable=False)
  password = db.Column('password', db.String(256), nullable=False)

  def __repr__(self):
    return '<Admin {}>'.format(self.id)
  
  def __init__(self, email, password):
    self.email = email
    self.password = password
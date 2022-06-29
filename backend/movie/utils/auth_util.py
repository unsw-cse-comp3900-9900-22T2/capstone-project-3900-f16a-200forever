import time
import jwt
from config import SECRET
import hashlib
from flask import session
import re

def generate_token(email):
  d = {
    'data': {
      'email': email,
      'timestamp': time.time()
    }
  }
  token = jwt.encode(d, SECRET, algorithm='HS256')

  return token


def pw_encode(password):
  '''
  It will encode raw password by sha256 from hashlib.
  Args:
      password (string): raw password
  Return:
      (string) encoded password
  '''
  return hashlib.sha256(password.encode()).hexdigest()

def user_is_valid(data):
  email = data['email']
  token = data['token']
  real_token = session[email]["token"]
  print(real_token)
  if real_token != token:
    return False
  return True

def user_is_admin(email):
  if session[email]['admin']:
    return True
  return False

def check_correct_answer(value):
  if value != 1 and value != 2 and value != 3:
    return False
  return True
    
def user_has_login(email, session):
  if email not in session.keys():
    return False
  return True

def correct_email_format(email):
  pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
  if re.fullmatch(pattern, email):
    return True
  return False
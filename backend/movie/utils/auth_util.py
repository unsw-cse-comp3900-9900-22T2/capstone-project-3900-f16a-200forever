import time
import jwt
from config import SECRET
import hashlib
from flask import session

def generate_token(email):
  d = {
    'iat': time.time(),
    'iss': 'Issuer',
    'data': {
      'email': email,
      'timestamp': time.time()
    }
  }
  return jwt.encode(d, SECRET, algorithm='HS256')


def pw_encode(password):
  '''
  It will encode raw password by sha256 from hashlib.
  Args:
      password (string): raw password
  Return:
      (string) encoded password
  '''
  return hashlib.sha256(password.encode()).hexdigest()

def user_is_valid(email, token):
  real_token = session[email]["token"]
  print(real_token)
  if real_token != token:
    return False
  return True

def user_is_admin(email):
  return session[email]['admin']

def check_correct_answer(value):
  if value != 1 and value != 2 and value != 3:
    return False
  return True
    
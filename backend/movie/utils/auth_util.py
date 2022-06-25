import time
import jwt
from config import SECRET
import hashlib

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

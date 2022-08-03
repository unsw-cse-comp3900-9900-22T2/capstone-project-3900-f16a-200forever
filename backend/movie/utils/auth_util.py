import time
import jwt
from config import SECRET, EMAIL
import hashlib
from flask import session
import re
from movie import db, redis_cli
from movie.models import user as User
from movie.models import admin as Admin
import smtplib
from email.mime.text import MIMEText
import math, random
from movie import smptyserver
 
def generateOTP():
  """
  generate 4 digit verfication code
  """
  digits = "0123456789"
  OTP = ""
  for i in range(4) :
    OTP += digits[math.floor(random.random() * 10)]
 
  return OTP

def send_email(email, code):
  msg = MIMEText(str(code))
  msg['Subject'] = 'The verfication code from Movie Forever' 
  msg['From'] = EMAIL
  msg['To'] = email
  smptyserver.sendmail(EMAIL, [email], msg.as_string())

def generate_token(email):
  d = {
    'data': {
      'email': email,
      'timestamp': time.time()
    }
  }
  token = jwt.encode(d, SECRET, algorithm='HS256').decode('utf-8')
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




def user_is_admin(email):
  user = db.session.query(Admin.Admins).filter(Admin.Admins.email == email).first()
  if user != None:
    return True
  return False

def check_correct_answer(value):
  if value != 1 and value != 2 and value != 3:
    return False
  return True






def check_auth(email, token):
  real = redis_cli.get(email)
  if real == None:
    return "the user has not logined", False
  real = str(real.decode())
  if real != token:
    return "the token is incorrect", False
  return "", True
  
def correct_email_format(email):
  pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
  if re.fullmatch(pattern, email):
    return True
  return False

def email_exits(email):
  user = db.session.query(User.Users).filter(User.Users.email == email).first()
  if user != None:
    return True
  user = db.session.query(Admin.Admins).filter(Admin.Admins.email == email).first()
  if user != None:
    return True
  return False
  

def username_format_valid(name):
  if len(name) < 6:
    return False
  if len(name) > 20:
    return False
  return True

def username_is_unique(name):
  user = db.session.query(User.Users).filter(User.Users.name == name).first()
  if user == None:
    return True
  return False

def correct_password_format(pw):
  if len(pw) < 8:
    return False
  return True

def code_is_correct(user, code):
  if user.validation_code != None and str(code) == str(user.validation_code):
    # invlaid the code
    user.validation_code = None
    db.session.commit()
    return True
  return False


def get_user(email, is_admin):
  curr_user = None
  if not is_admin:
    curr_user = db.session.query(User.Users).filter(User.Users.email == email).first()
  elif is_admin:
    curr_user = db.session.query(Admin.Admins).filter(Admin.Admins.email == email).first()
  return curr_user

def password_is_correct(user, pw):
  if pw_encode(pw) != user.password:
    return True
  return False

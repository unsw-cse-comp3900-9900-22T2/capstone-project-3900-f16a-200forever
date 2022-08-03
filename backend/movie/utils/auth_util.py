import time
import jwt
from config import SECRET, EMAIL
import hashlib
from flask import session
import re
from movie import db, redis_cli
from movie.models import user as User
from movie.models import admin as Admin
from email.mime.text import MIMEText
import math, random
from movie import smptyserver
 
# It will generate a random code and save it to the user.
# Args: none
# Return:
#     (string) random code
def generateOTP():
  digits = "0123456789"
  OTP = ""
  for i in range(4) :
    OTP += digits[math.floor(random.random() * 10)]
 
  return OTP

# It will send a email to the user.
# Args:
#     email (string): user email
#     code (string): verification code
def send_email(email, code):
  msg = MIMEText(str(code))
  msg['Subject'] = 'The verfication code from Movie Forever' 
  msg['From'] = EMAIL
  msg['To'] = email
  smptyserver.sendmail(EMAIL, [email], msg.as_string())

# It will generate a token for the user.
# Args:
#     email (string): user email
# Return:
#     token
def generate_token(email):
  d = {
    'data': {
      'email': email,
      'timestamp': time.time()
    }
  }
  token = jwt.encode(d, SECRET, algorithm='HS256').decode('utf-8')
  return token

# It will encode raw password by sha256 from hashlib.
# Args:
#     password (string): raw password
# Return:
#     (string) encoded password
def pw_encode(password):
  return hashlib.sha256(password.encode()).hexdigest()

# It will give a result to tell if the user is admin or not.
# Args:
#     email (string): user email
# Return:
#     (boolean) True if the user is admin, False otherwise
def user_is_admin(email):
  user = db.session.query(Admin.Admins).filter(Admin.Admins.email == email).first()
  if user != None:
    return True
  return False

# It will check if the answer is right
# Args:
#     value (int): the answer
# Return:
#     (boolean) True if the answer is valid, False otherwise
def check_correct_answer(value):
  print(value)
  if value <=1 or value >3:
    return False
  return True

# It will check if the user is an auth
# Args:
#     email (string): user email
#     token: token
# Return:
#     (boolean) True if the user is auth, False otherwise
def check_auth(email, token):
  real = redis_cli.get(email)
  if real == None:
    return "the user has not logined", False
  real = str(real.decode())
  if real != token:
    return "the token is incorrect", False
  return "", True
  
# It will check if the email is valid
# Args:
#     email (string): user email
# Return:
#     (boolean) True if the email is valid, False otherwise
def correct_email_format(email):
  pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
  if re.fullmatch(pattern, email):
    return True
  return False

# It will check if the email exists in the database
# Args:
#     email (string): user email
# Return:
#     (boolean) True if the email exists, False otherwise
def email_exits(email):
  user = db.session.query(User.Users).filter(User.Users.email == email).first()
  if user != None:
    return True
  user = db.session.query(Admin.Admins).filter(Admin.Admins.email == email).first()
  if user != None:
    return True
  return False
  
# It will check if the username is valid
# Args:
#     name (string): user name
# Return:
#     (boolean) True if the username is valid, False otherwise
def username_format_valid(name):
  if len(name) < 6:
    return False
  if len(name) > 20:
    return False
  return True

# It will check if the username is unique
# Args:
#     name (string): user name
# Return:
#     (boolean) True if the username is unique, False otherwise
def username_is_unique(name):
  user = db.session.query(User.Users).filter(User.Users.name == name).first()
  if user == None:
    return True
  return False

# It will check if the password's format is correct
# Args:
#     pw (string): user password
# Return:
#     (boolean) True if the password's format is correct, False otherwise
def correct_password_format(pw):
  if len(pw) < 8:
    return False
  return True

# It will check if the code is correct
# Args:
#    user: user object
#    code (string): verification code
# Return:
#    (boolean) True if the code is correct, False otherwise
def code_is_correct(user, code):
  if user.validation_code != None and str(code) == str(user.validation_code):
    # invlaid the code
    user.validation_code = None
    db.session.commit()
    return True
  return False

# It will get the user
# Args:
#     email (string): user email
# Return:
#     (object) user object
def get_user(email, is_admin):
  curr_user = None
  if not is_admin:
    curr_user = db.session.query(User.Users).filter(User.Users.email == email).first()
  elif is_admin:
    curr_user = db.session.query(Admin.Admins).filter(Admin.Admins.email == email).first()
  return curr_user

# It will check if the password is correct
# Args:
#     user: user object
#     pw (string): user password
# Return:
#     (boolean) True if the password is correct, False otherwise
def password_is_correct(user, pw):
  if pw_encode(pw) != user.password:
    return True
  return False

from movie.utils.other_until import convert_object_to_dict, convert_model_to_dict
from sqlalchemy import inspect
from movie import db
import movie.models.user as User

def user_id_valid(id):
  user = db.session.query(User.Users).filter(User.Users.id == id).first()
  print(user)
  if user == None:
    return False
  return True

def get_user_id(email):
  user = db.session.query(User.Users).filter(User.Users.email == email).first()
  if user == None:
    raise Exception("User doesn't exist")
  return user.id
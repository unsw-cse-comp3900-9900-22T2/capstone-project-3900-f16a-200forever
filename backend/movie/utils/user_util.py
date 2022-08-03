from movie.utils.other_until import convert_object_to_dict, convert_model_to_dict
from sqlalchemy import inspect
from movie import db
import movie.models.user as User
import movie.models.admin as Admin

def user_id_valid(id):
  user = db.session.query(User.Users).filter(User.Users.id == id).first()
  print(user)
  if user == None:
    return False
  return True

def get_admin_id(email):
  user = db.session.query(Admin.Admins).filter(Admin.Admins.email == email).first()
  if user == None:
    raise Exception("Admin doesn't exist")
  return user.id

def get_user_id(email):
  user = db.session.query(User.Users).filter(User.Users.email == email).first()
  if user == None:
    raise Exception("User doesn't exist")
  return user.id

def get_user_email(id):
  user = db.session.query(User.Users).filter(User.Users.id == id).first()
  if user == None:
    raise Exception("User doesn't exist")
  return user.email

# Unordered TODO find out what order to do, fix formatting
# Returns a list of movies in user wishlist
def get_wishlist(id):
  results = db.session.query(User.MovieWishLis).filter(User.MovieWishLis.user_id == id).all()
  wishlist = []
  for movie in results:
    wishlist.append(movie.movie_id)

  return wishlist


def get_watchedlist(id):
  results = db.session.query(User.MovieWatchedList).filter(User.MovieWatchedList.user_id == id).all()
  watchedlist = []
  for movie in results:
    watchedlist.append(movie.movie_id)

  return watchedlist


def get_droppedlist(id):
  results = db.session.query(User.MovieDroppedList).filter(User.MovieDroppedList.user_id == id).all()
  droppedlist = []
  for movie in results:
    droppedlist.append(movie.movie_id)

  return droppedlist


def get_badges(id):
  results = db.session.query(User.UserEvent).filter(User.UserEvent.user_id == id).filter(User.UserEvent.event_status.like(f'%passed%')).all()
  badges = []
  for badge in results:
    badges.append(badge.event_id)
  return badges

def get_image(image):
  if image is not None:
      return str(image.decode())
  return image
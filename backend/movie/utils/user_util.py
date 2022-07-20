from movie.utils.other_until import convert_object_to_dict, convert_model_to_dict
from sqlalchemy import inspect
from movie import db
<<<<<<< HEAD
import movie.models.user as Users
=======
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

def get_user_email(id):
  user = db.session.query(User.Users).filter(User.Users.id == id).first()
  if user == None:
    raise Exception("User doesn't exist")
  return user.email
>>>>>>> 6369f1e2e8e00181e2c83438758c7285e2c4948e

# Unordered TODO find out what order to do, fix formatting
# Returns a list of movies in user wishlist
def get_wishlist(id):
<<<<<<< HEAD
  results = db.session.query(Users.WishlistMovie).filter(Users.WishlistMovie.user_id == id).all()
  wishlist = []
  for movie in results:
    wishlist.append(movie)
=======
  results = db.session.query(User.WishlistMovie).filter(User.WishlistMovie.user_id == id).all()
  wishlist = []
  for movie in results:
    wishlist.append(movie.movie_id)
>>>>>>> 6369f1e2e8e00181e2c83438758c7285e2c4948e

  return wishlist


def get_watchedlist(id):
<<<<<<< HEAD
  results = db.session.query(Users.WatchedlistMovie).filter(Users.WatchedlistMovie.user_id == id).all()
  watchedlist = []
  for movie in results:
    watchedlist.append(movie)
=======
  results = db.session.query(User.WatchedlistMovie).filter(User.WatchedlistMovie.user_id == id).all()
  watchedlist = []
  for movie in results:
    watchedlist.append(movie.movie_id)
>>>>>>> 6369f1e2e8e00181e2c83438758c7285e2c4948e

  return watchedlist


def get_droppedlist(id):
<<<<<<< HEAD
  results = db.session.query(Users.DroppedlistMovie).filter(Users.DroppedlistMovie.user_id == id).all()
  droppedlist = []
  for movie in results:
    droppedlist.append(movie)
=======
  results = db.session.query(User.DroppedlistMovie).filter(User.DroppedlistMovie.user_id == id).all()
  droppedlist = []
  for movie in results:
    droppedlist.append(movie.movie_id)
>>>>>>> 6369f1e2e8e00181e2c83438758c7285e2c4948e

  return droppedlist


def get_badges(id):
<<<<<<< HEAD
  results = db.session.query(Users.UserEvent).filter(Users.UserEvent.user_id == id).all()
  badges = []
  for badge in badges:
    badges.append(badge)

  return badges
=======
  results = db.session.query(User.UserEvent).filter(User.UserEvent.user_id == id).filter(User.UserEvent.event_status.like(f'%passed%')).all()
  badges = []
  for badge in results:
    badges.append(badge.event_id)
  return badges
>>>>>>> 6369f1e2e8e00181e2c83438758c7285e2c4948e

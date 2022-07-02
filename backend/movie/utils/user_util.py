from movie.utils.other_until import convert_object_to_dict, convert_model_to_dict
from sqlalchemy import inspect
from movie import db
import movie.models.user as Users

# Unordered TODO find out what order to do, fix formatting
# Returns a list of movies in user wishlist
def get_wishlist(id):
  results = db.session.query(Users.WishlistMovie).filter(Users.WishlistMovie.user_id == id).all()
  wishlist = []
  for movie in results:
    wishlist.append(movie)

  return wishlist


def get_watchedlist(id):
  results = db.session.query(Users.WatchedlistMovie).filter(Users.WatchedlistMovie.user_id == id).all()
  watchedlist = []
  for movie in results:
    watchedlist.append(movie)

  return watchedlist


def get_droppedlist(id):
  results = db.session.query(Users.DroppedlistMovie).filter(Users.DroppedlistMovie.user_id == id).all()
  droppedlist = []
  for movie in results:
    droppedlist.append(movie)

  return droppedlist


def get_badges(id):
  results = db.session.query(Users.UserEvent).filter(Users.UserEvent.user_id == id).all()
  badges = []
  for badge in badges:
    badges.append(badge)

  return badges

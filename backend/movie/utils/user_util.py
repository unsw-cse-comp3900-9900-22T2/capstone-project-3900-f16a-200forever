from movie.utils.other_util import convert_object_to_dict, convert_model_to_dict
from sqlalchemy import inspect
from movie import db
import movie.models.user as User
import movie.models.admin as Admin
import movie.models.event as Event

# check the user exist or not
def user_id_valid(id):
  user = db.session.query(User.Users).filter(User.Users.id == id).first()
  print(user)
  if user == None:
    return False
  return True

# get the id of the admin
def get_admin_id(email):
  user = db.session.query(Admin.Admins).filter(Admin.Admins.email == email).first()
  if user == None:
    #raise Exception("Admin doesn't exist")
    return None
  return user.id

# get the id of the user
def get_user_id(email):
  user = db.session.query(User.Users).filter(User.Users.email == email).first()
  if user == None:
    #raise Exception("User doesn't exist")
    return None
  return user.id

# get the email of the user
def get_user_email(id):
  user = db.session.query(User.Users).filter(User.Users.id == id).first()
  if user == None:
    raise Exception("User doesn't exist")
  return user.email

# get the wishlistdlist of the given user
# id: id of the user
# wishlist: the list of movie id
def get_wishlist(id):
  results = db.session.query(User.MovieWishList).filter(User.MovieWishList.user_id == id).all()
  wishlist = []
  for movie in results:
    wishlist.append(movie.movie_id)

  return wishlist

# get the watchedlist of the given user
# id: id of the user
# watchedlist: the list of movie id
def get_watchedlist(id):
  results = db.session.query(User.MovieWatchedList).filter(User.MovieWatchedList.user_id == id).all()
  watchedlist = []
  for movie in results:
    watchedlist.append(movie.movie_id)

  return watchedlist


# get the dropped list of the given user
# id: id of the user
# droppedlist: the list of movie id
def get_droppedlist(id):
  results = db.session.query(User.MovieDroppedList).filter(User.MovieDroppedList.user_id == id).all()
  droppedlist = []
  for movie in results:
    droppedlist.append(movie.movie_id)

  return droppedlist

# get all the event that the user pass
# id: id of the user
# badges: the list of the event id
def get_badges(id):
  results = db.session.query(User.UserEvent, Event.Events).filter(User.UserEvent.user_id == id, Event.Events.id == User.UserEvent.event_id).filter(User.UserEvent.event_status.like(f'%passed%')).all()
  badges = []
  for badge in results:
    tmp = convert_object_to_dict(badge[1])
    tmp['image'] = get_image(tmp['image'])
    badges.append(tmp)
  return badges

# get the username of the give user
# id: the id of the user
def current_username(id):
  user = db.session.query(User.Users).filter(User.Users.id == id).first()
  return user.name

# decode the image and convert into string
# arg image: byte type
def get_image(image):
  if image is not None:
      return str(image.decode())
  return image
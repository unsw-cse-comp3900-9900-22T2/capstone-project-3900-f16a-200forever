from operator import is_
from attr import validate
from movie.utils.auth_util import username_is_unique, username_format_valid, correct_password_format, password_is_correct, pw_encode
from numpy import require, str_
from sqlalchemy import true
from movie.models import user as User
from movie import app, request
from flask import session, jsonify
from json import dumps
from flask_restx import Resource, reqparse
from movie import db
from .api_models import UserNS
from movie.utils.user_util import get_wishlist, get_watchedlist, get_droppedlist, get_badges, get_user_email

user_ns = UserNS.user_ns

# user profile page
@user_ns.route('/userprofile')
class UserProfileController(Resource):
  @user_ns.response(200, "User profile success")
  @user_ns.response(400, "Something wrong")
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, required=True, location="args")
    args = parser.parse_args()
    print(args)
    user_id = args['user_id']

    this_user = db.session.query(User.Users).filter(User.Users.id == user_id).first()
    if this_user == None:
      print("none")
      return {"message": "User doesn\'t exist"}, 400

    username = this_user.name
    profile_picture = this_user.image
    signature = this_user.signature
    wishlist = get_wishlist(user_id)
    watchedlist = get_watchedlist(user_id)
    droppedlist = get_droppedlist(user_id)
    badges = get_badges(user_id)

    # id, username, profile picture, signature, wishlist, watchlist, droplist, badges
    user_profile = {
      'id': user_id, #str
      'username': username, #str
      'profile_picture': profile_picture, #str
      'signature': signature, #str
      'wishlist': wishlist, #list
      'watchedlist': watchedlist, #list
      'droppedlist': droppedlist, #list
      'badges': badges #list
    }
    return user_profile, 200

  @user_ns.response(200, "Edit profile success")
  @user_ns.response(400, "Something wrong")
  @user_ns.expect(UserNS.user_edit_profile, validate=True)
  def put(self):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, required=True, location="args")
    args = parser.parse_args()
    print(args)
    user_id = args['user_id']
    email = get_user_email(user_id)

    # check if logged in
    '''if not user_has_login(email, session):
      return {"message": "the user has not logined"}, 400

    # check token
    if not user_is_valid(data):
      return {"message": "Invalid user id"}, 400'''

    this_user = db.session.query(User.Users).filter(User.Users.id == user_id).first()
    if this_user == None:
      print("none")
      return {"message": "User doesn\'t exist"}, 400

    data = user_ns.payload
    username = data['username']
    signature = data['signature']
    image = data['image']
    current_password = None
    new_password = None

    # check password fields
    if ('current_password' in data and not 'new_password' in data) or (not 'current_password' in data and 'new_password' in data):
      return {"message": "Need both passwords"}, 400
      
    if 'current_password' in data and 'new_password' in data:
      current_password = data['current_password']
      new_password = data['new_password']

    if not username_format_valid(username):
      return {"message": "Username must be 6-20 characters"}, 400

    if not username_is_unique(username):
      return {"message": "Username already taken"}, 400

    if current_password != None and new_password != None:
      if not correct_password_format(new_password):
        return {"message": "The password is too short, at least 8 characters"}, 400

      if password_is_correct(this_user, current_password):
        return {"message": "Incorrect password"}, 400

      if current_password == new_password:
        return {"message": "New password cannot be the same as the old"}, 400

      this_user.password = pw_encode(new_password)

    this_user.name = username
    this_user.signature = signature
    #this_user.image = image
    db.session.commit()

    return {
        "message": "Edit profile success"
    }, 200
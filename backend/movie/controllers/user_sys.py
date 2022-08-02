from operator import is_
import sqlite3
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
from movie.utils.other_until import convert_model_to_dict, convert_object_to_dict
from movie.utils.user_util import get_wishlist, get_watchedlist, get_droppedlist, get_badges, get_user_email, current_username
from movie.utils.auth_util import user_has_login, user_is_valid
import sqlite3
user_ns = UserNS.user_ns

@user_ns.route("/events")
class UserEvent(Resource):
  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, location='args', required=True)
    args = parser.parse_args()
    email = args['email']

    # 1. check the user is valid or not
    user = db.session.query(User.Users).filter(User.Users.email == email).first()
    if user == None:
      return {"message": "the user not exist"},400

    return {"events": convert_model_to_dict(user.events)}, 200
    
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
    image = None
    if profile_picture is not None:
      image = str(profile_picture.decode())
    
    user_profile = {
      'id': user_id, #str
      'username': username, #str
      'profile_picture': image, #str
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
    user_id = args['user_id']
    data = user_ns.payload
    email = data['email']
    """
    # check if logged in
    if not user_has_login(email, session):
      return {"message": "the user has not logined"}, 400

    # check token
    if not user_is_valid(data):
      return {"message": "Token is not correct"}, 400
    """


    this_user = db.session.query(User.Users).filter(User.Users.id == user_id).first()
    if this_user == None:
      return {"message": "User doesn\'t exist"}, 400
    
    if this_user.email != email:
      return {"message": "No permission"}, 400

    username = data['username']

    # check user name
    if not username_format_valid(username):
      return {"message": "Username must be 6-20 characters"}, 400

    if not username_is_unique(username) and not current_username(user_id) == username:
      return {"message": "Username already taken"}, 400

    # edit pw
    if "current_password" in data.keys():
      # incorrect
      if pw_encode(data['current_password']) != this_user.password:
        return {"message": "Incorrect password"}, 400

      # correct
      if "double_check" in data.keys() and "new_password" in data.keys():
        if not correct_password_format(data['new_password']):
          return {"message": "password formact not correct"}, 400
        if data['double_check'] != data['new_password']:
          return {"message": "2 password are not the same"}, 400
        this_user.password = pw_encode(data['new_password'])

    this_user.name = username
    # 
    if 'signature' in data.keys():
      this_user.signature = data['signature']
    if 'image' in data.keys():
      this_user.image = data['image'].encode()
    db.session.commit()

    return {
        "message": "Edit profile success"
    }, 200

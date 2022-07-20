from operator import is_
from attr import validate
from numpy import require, str_
from sqlalchemy import true
from movie.models import user as User
from movie import app, request
from flask import session, jsonify
from json import dumps
from flask_restx import Resource, reqparse
from movie import db
from .api_models import UserNS
from movie.utils.user_util import get_wishlist, get_watchedlist, get_droppedlist, get_badges

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

    this_user = db.session.query(User.Users).filter(User.Users.id == user_id).first()
    if this_user == None:
      print("none")
      return {"message": "User doesn\'t exist"}, 400

    # editing is which attribute the user wants to edit
    # info is what they want to edit it to
    data = user_ns.payload
    editing = data['editing']
    info = data['info']

    # check if logged in
    '''if not user_has_login(email, session):
      return {"message": "the user has not logined"}, 400

    # check token
    if not user_is_valid(data):
      return {"message": "Invalid user id"}, 400'''

    if editing == "username":
      exists = db.session.query(User.Users).filter(User.Users.name == info).first()
      if exists != None:
        return {'message': 'Username already taken'}, 400
      this_user.name = info
      db.session.commit()
      return {"message": "Successfully updated username"}, 200

    if editing == "profile picture":
      this_user.image = info
      db.session.commit()
      return {"message": "Successfully updated profile picture"}, 200

    if editing == "signature":
      this_user.signature = info
      db.session.commit()
      return {"message": "Successfully updated signature"}, 200

    return {
        "message": "Edit profile error"
    }, 400
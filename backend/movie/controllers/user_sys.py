import imp
from .api_models import UserNs
from flask_restx import Resource, reqparse
from movie.models import user as User
from movie import db
from movie.utils.other_until import convert_model_to_dict, convert_object_to_dict
from movie.utils.auth_util import user_has_login, user_is_valid
from movie import db
from flask import session

user_ns = UserNs.user_ns

@user_ns.route("/events")
class UserEvent(Resource):
  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  def get(self):
    """
    get all events of the user
    """
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, location='args', required=True)
    args = parser.parse_args()
    email = args['email']

    # 1. check the user is valid or not
    user = db.session.query(User.Users).filter(User.Users.email == email).first()
    if user == None:
      return {"message": "the user not exist"},400

    return {"events": convert_model_to_dict(user.events)}, 200

@user_ns.route("/followlist")
class FollowListManage(Resource):
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
    
    result = []
    for fo in user.user_follow_list:
      user = fo.follower
      data = {}
      data['email'] = user.email
      data['image'] = user.image
      data['id'] = user.id
      data['name'] = user.name
      result.append(data)

    return {"list": result}, 200

  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  @user_ns.expect(UserNs.follow_form, validate=True)
  def post(self):
    data = user_ns.payload

    # check user login
    if not user_has_login(data['email'], session):
      return {"message": "the user has not logined"}, 400

    # check token valid
    if not user_is_valid(data):
      return {"message": "the token is incorrect"}, 400

    # check follow itself
    if data['email'] == data['follow_email']:
      return {"message": "Cannot follow self"}, 400

    # check follow valid
    follow = db.session.query(User.Users).filter(User.Users.email == data['follow_email']).first()
    if follow == None:
      return {"message": "Follow email invalid"}, 400

    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
    
    # check has follow
    try:
      tmp = {"user_id": user.id, "follow_id": follow.id}
      new = User.FollowList(tmp)
      db.session.add(new)
      db.session.commit()
    except:
      db.session.rollback()
      return {"message": "Has followed already"}, 400
    return {"message": "Successfully"}, 200

  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  @user_ns.expect(UserNs.follow_form, validate=True)
  def delete(self):
    data = user_ns.payload

    # check user login
    if not user_has_login(data['email'], session):
        return {"message": "the user has not logined"}, 400

    # check token valid
    if not user_is_valid(data):
        return {"message": "the token is incorrect"}, 400

    # check follow valid
    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()

    follow = db.session.query(User.Users).filter(User.Users.email == data['follow_email']).first()
    if follow == None:
      return {"message": "Follow email invalid"}, 400
    


    db.session.delete(follow_rel)
    db.session.commit()
    return {"message": "Successfully"}, 200

@user_ns.route("/followlist/reviews")
class FollowReview(Resource):
  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  @user_ns.expect(UserNs.follow_form, validate=True)
  def post(self):
    data = user_ns.payload

    # check user login
    if not user_has_login(data['email'], session):
        return {"message": "the user has not logined"}, 400

    # check token valid
    if not user_is_valid(data):
        return {"message": "the token is incorrect"}, 400

    # check the user in the follow list
    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
    if user == None:
      return {'message': "invalid user email"}, 400

    follow = db.session.query(User.Users).filter(User.Users.email == data['follow_email']).first()
    if follow == None:
      return {"message": "Haven't followed"}, 400

    follow_rel = db.session.query(User.FollowList).filter(User.FollowList.user_id == user.id, User.FollowList.follow_id == follow.id).first()
    if follow_rel == None:
      return {"message": "Haven't followed before"}, 400

    # get the reviews 
    result = follow.reviews
    result.sort(key=lambda x: x.created_time)
    result.reverse()
    
    return {"reviews": convert_model_to_dict(result)}, 200
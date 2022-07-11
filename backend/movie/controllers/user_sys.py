import imp
from .api_models import UserNs
from flask_restx import Resource, reqparse
from movie.models import user as User
from movie import db
from movie.utils.other_until import convert_model_to_dict, convert_object_to_dict

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

    


import imp
from .api_models import UserNs
from flask_restx import Resource, reqparse
from movie.models import user as User
from movie import db
from movie.utils.other_until import convert_model_to_dict

user_ns = UserNs.user_ns

@user_ns.route("/event")
class UserEvent(Resource):
  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  def get(self):
    """
    get all events of the user
    """
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str, location='args', required=True)
    args = parser.parse_args()
    id = args['id']

    # 1. check the user is valid or not
    user = db.session.query(User.Users).filter(User.Users.id == id).first()
    if user == None:
      return {"message": "the user not exist"},400

    return {"events": convert_model_to_dict(user.events)}, 200

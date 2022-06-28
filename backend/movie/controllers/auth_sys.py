from operator import is_
from attr import validate
from numpy import require, str_
from movie.models import user as User
from movie import app, request
from flask import session
from flask_restx import Resource
from json import dumps
from flask_restx import Resource, Api
from movie.utils.auth_util import generate_token, pw_encode, user_is_valid, user_has_login
from movie import db
from movie.models import admin as Admin

from .api_models import AuthNS, AdminNS


auth_ns = AuthNS.auth_ns
admin_ns = AdminNS.admin_ns

@auth_ns.route('/login')
class LoginController(Resource):
  @auth_ns.response(200, "Login Successfully")
  @auth_ns.response(400, "Something wrong")
  @auth_ns.expect(AuthNS.auth_login, validate=True)
  def post(self):
    data = auth_ns.payload
    email = data['email']
    pw = data['password']
    is_admin = data['is_admin']

    # check the user has login or not
    if email in session.keys():
      return dumps({"message": "The user has logined"}), 400

    curr_user = None
    if is_admin == "False":
      curr_user = db.session.query(User.Users).filter(User.Users.email == email).first()
    elif is_admin == 'True':
      curr_user = db.session.query(Admin.Admins).filter(Admin.Admins.email == email).first()
    else:
      return dumps({"message": "is_admin ust be True or False"}), 400
    # check the user is valid or not
    if curr_user == None:
      return dumps({"message": "The user not registe"}), 400
    
    if pw_encode(pw) != curr_user.password:
      return dumps({"message": "Wrong password"}), 400

    token = generate_token(email)
    print(token)
    session[email] = {'token': token, "id": curr_user.id, "admin": is_admin}
    return dumps({
        'token': generate_token(email)
    }), 200
  
@auth_ns.route('/logout')
class logoutController(Resource):
  @auth_ns.response(200, "Logout successfullly")
  @auth_ns.response(400, "Something wrong")
  @auth_ns.expect(AuthNS.auth_logout, validate=True)
  def post(self):
    data = auth_ns.payload

    if not user_has_login(data['email'], session):
      return {"message": "the user has not logined"}, 400

    
    if not user_is_valid(data):
      return {"message": "the token is incorrect"}, 400

    session.pop(data['email'])
    return {"message": "logout successfully"}, 200

    
from attr import validate
from numpy import require
from movie.models import user
from movie import app, request
from flask import session
from flask_restx import Resource, reqparse
from json import dumps
from flask_restx import Resource, Api
from movie.utils.auth_util import generate_token, pw_encode
from movie import db
from movie.models import admin

from .api_models import AuthNS, AdminNS

from flask_restx import Namespace, fields

auth_ns = AuthNS.auth_ns
admin_ns = AdminNS.admin_ns

@auth_ns.route('/login')
@admin_ns.route('/login')
class LoginController(Resource):
  @auth_ns.response(200, "Login Successfully")
  @auth_ns.response(400, "TODO")
  @auth_ns.expect(AuthNS.auth_login)
  @admin_ns.response(200, "Login Successfully")
  @admin_ns.response(400, "TODO")
  @admin_ns.expect(AuthNS.auth_login, validate=True)
  def post(self):
    data = request.get_json()

    email = data['email']
    pw = data['password']
    is_admin = data['auth']
    print(email)
    curr_user = None
    if not is_admin:
      curr_user = db.session.query(user.Users).filter(user.Users.email == email).first()
    else:
      curr_user = db.session.query(admin.Admins).filter(admin.Admins.email == email).first()
    if curr_user == None:
      #TODO: response status
      return 400
    
    #encode the password
    if pw_encode(pw) != user.password:
      #TODO: response status
      return 400

    token = generate_token(email)
    session[email] = token
    session["id"] = user.id
    return dumps({
        'token': generate_token(email)
    }), 200
  
@admin_ns.route('/logout')
@auth_ns.route('/logout')
class logoutController(Resource):
  @admin_ns.response(200, "Logout successfullly")
  @admin_ns.response(400, "TODO")
  @admin_ns.expect(AdminNS.admin_logout, validate=True)
  @auth_ns.response(200, "Logout successfullly")
  @auth_ns.response(400, "TODO")
  @auth_ns.expect(AuthNS.auth_logout, validate=True)
  def post(self):
    data = request.get_json()
    email = data['email']

    if email not in session.keys():
      #TODO:
      return {"message": "the user has not logined"}, 400

    session.pop(email)
    return {"message": "logout successfully"}, 200
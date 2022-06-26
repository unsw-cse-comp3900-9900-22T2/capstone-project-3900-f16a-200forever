from numpy import require
from movie.models import users
from movie import app, request
from flask import session
from flask_restx import Resource, reqparse
from json import dumps
from flask_restx import Resource, Api
from movie.utils.auth_util import generate_token, pw_encode
from movie import db
from movie.models import admins

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
  @admin_ns.expect(AuthNS.auth_login)
  def post(self):
    req_parse = reqparse.RequestParser(bundle_errors=True)
    req_parse.add_argument('email', required=True, type=str)
    req_parse.add_argument('password', required=True, type=str)
    args = req_parse.parse_args()

    email = args.get('email')
    pw = args.get('password')
    is_admin = args.get('auth')

    print(args)

    user = None
    if not is_admin:
      user = db.session.query(users.Users).filter(users.Users.email == email).first()
    else:
      user = db.session.query(admins.Admins).filter(admins.Admins.email == email).first()
    if user == None:
      #TODO: response status
      return 400
    
    #encode the password
    if pw_encode(pw) != user.password:
      print(pw_encode(pw))
      #TODO: response status
      return 400

    token = generate_token(email)
    session[email] = token
    return dumps({
        'token': generate_token(email)
    }), 200
  
@admin_ns.route('/logout')
@auth_ns.route('/logout')
class logoutController(Resource):
  @admin_ns.response(200, "Logout successfullly")
  @admin_ns.response(400, "TODO")
  @admin_ns.expect(AdminNS.admin_logout)
  @auth_ns.response(200, "Logout successfullly")
  @auth_ns.response(400, "TODO")
  @auth_ns.expect(AuthNS.auth_logout)
  def post(self):
    req_parse = reqparse.RequestParser(bundle_errors=True)
    req_parse.add_argument('email', required=True, type=str)
    args = req_parse.parse_args()
    email = args.get('email')

    if email not in session.keys():
      #TODO:
      return {"message": "the user has not logined"}, 400

    session.pop(email)
    return {"message": "logout successfully"}, 200
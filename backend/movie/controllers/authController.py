from numpy import require
from movie.models import users
from movie import app, request
from flask import session
from flask_restx import Resource, reqparse
from json import dumps
from flask_restx import Resource, Api
from movie.utils.auth_util import generate_token, pw_encode
from movie import db

from .api_models import AuthNS

from flask_restx import Namespace, fields

auth_ns = AuthNS.auth_ns

#auth_ns = AuthAPI.auth_ns

@auth_ns.route('/login')
class LoginController(Resource):
  @auth_ns.response(201, "login")
  @auth_ns.expect(AuthNS.auth_login)
  def post(self):
    req_parse = reqparse.RequestParser(bundle_errors=True)
    req_parse.add_argument('email', required=True, type=str)
    req_parse.add_argument('password', required=True, type=str)
    args = req_parse.parse_args()

    email = args.get('email')
    pw = args.get('password')
    #TODO:

    print(db.session.query(users.Users).all())
    user = db.session.query(users.Users).filter(users.Users.email == email).first()
    if user == None:
      #TODO:
      pass
    
    #TODO: encode the password
    if pw != user.password:
      #TODO:
      pass

    token = generate_token(email)
    session[email] = token
    return dumps({
        'token': generate_token(email)
    }), 200
  



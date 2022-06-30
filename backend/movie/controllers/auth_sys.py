from operator import is_
from attr import validate
from numpy import require, str_
from sqlalchemy import true
from movie.models import user as User
from movie import app, request
from flask import session
from flask_restx import Resource
from json import dumps
from flask_restx import Resource, Api
from movie.utils.auth_util import generate_token, pw_encode, user_is_valid, \
                                  user_has_login, correct_email_format, \
                                  username_format_valid, username_is_unique, \
                                  email_exits, correct_password_format, generateOTP, \
                                  send_email, code_is_correct, get_user, password_is_correct
from movie import db
from movie.models import admin as Admin
from .api_models import AuthNS, AdminNS

auth_ns = AuthNS.auth_ns
admin_ns = AdminNS.admin_ns

@auth_ns.route('/sendemail')
class SendEmail(Resource):
  @auth_ns.response(200, "Send Email Successfully")
  @auth_ns.response(400, "Something wrong")
  @auth_ns.expect(AuthNS.auth_send_email, validate=True) 
  def post(self):
    data = auth_ns.payload
    email = data['email']

    # check email format
    if not correct_email_format(email):
      return dumps({"message": "Email format not correct"}), 400

    # check email has been registed or not
    if not email_exits(email):
      return dumps({"message": "The email has not been registered"}), 400

    # send vertification code
    code = str(generateOTP())
    try:
      send_email(email, code)
    except:
      return dumps({"message": "Send email failed, try again pls"}), 400

    # update validation code
    user = db.session.query(User.Users).filter(User.Users.email == email).first()
    user.validation_code = code
    db.session.commit()
    return dumps({"message": "code has been send"}), 200

@auth_ns.route('/reset_password')
class ResetPasswordController(Resource):
  @auth_ns.response(200, "Password reset")
  @auth_ns.response(400, "Something wrong")
  @auth_ns.expect(AuthNS.auth_reset_password, validate=True)
  def post(self):
    data = auth_ns.payload
    email = data['email']
    code = data['validation_code']
    current_pw = data['current_password']
    new_pw = data['new_password']
    confirm_new_pw = data['confirm_new_password']
    
    #check the token
    if not user_is_valid(data):
      return dumps({"message": "Invalid token"}), 400

    # check the validation code
    if code_is_correct(email, code):
      return dumps({"message": "Incorrect validation code"}), 400

    # check the user old password
    user = get_user(email, session[email]["is_admin"])
    if password_is_correct(user, current_pw):
      return dumps({"message": "Incorrect current password"}), 400

    # check password format
    if not correct_password_format(new_pw):
      return dumps({"message": "The password is too short, at least 8 characters"}), 400

    # check if confirm password is the same as the new password
    if new_pw != confirm_new_pw:
      return dumps({"message": "New passwords are not the same"}), 400

    # encode pw
    data['new_password'] = pw_encode(new_pw)

    # update db
    user.password = data['new_password']
    db.session.commit()

    return dumps({"message": "Password updated"}), 200


@auth_ns.route('/register')
class RegisterController(Resource):
  @auth_ns.response(200, "Login Successfully")
  @auth_ns.response(400, "Something wrong")
  @auth_ns.expect(AuthNS.auth_register, validate=True)
  def post(self):
    data = auth_ns.payload
    name = data['name']
    email = data['email']
    pw = data['password']

    # check email format
    if not correct_email_format(email):
      return dumps({"message": "Email format not correct"}), 400

    # check email has been registed or not
    if email_exits(email):
      return dumps({"message": "The email is already been registed"}), 400

    # check user name format
    if not username_format_valid(name):
      return dumps({"message": "Username must be 6-20 characters"}), 400
  
    # check user name has exist or not
    if not username_is_unique(name):
      return dumps({"message": "The username already exists"}), 400

    # check password format
    if not correct_password_format(pw):
      return dumps({"message": "The password is too short, at least 8 characters"}), 400

    #encode pw
    data['password'] = pw_encode(pw)
    # commit into db
    new_user = User.Users(data)
    db.session.add(new_user)
    db.session.commit()

    # generate token, save to redis
    token = generate_token(email)
    print(token)
    session[email] = {'token': token, "id": new_user.id, "admin": False}

    return dumps({
        'token': generate_token(email),
        'name': new_user.name
    }), 200

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

    # check email format
    if not correct_email_format(email):
      return dumps({"message": "Please enter correct email"}), 400
      
    # check the user has login or not
    if email in session.keys():
      return dumps({"message": "The user has logined"}), 400

    curr_user = get_user(email, is_admin)
    # check the user is valid or not
    if curr_user == None:
      return dumps({"message": "The user not registered"}), 400
    
    if password_is_correct(curr_user, pw):
      return dumps({"message": "Wrong password"}), 400

    token = generate_token(email)
    print(token)
    session[email] = {'token': token, "id": curr_user.id, "admin": is_admin}

    return dumps({
        'token': token,
        'name': curr_user.name
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

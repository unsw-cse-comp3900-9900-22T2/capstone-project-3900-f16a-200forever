from movie.models import user as User
from flask_restx import Resource
from flask_restx import Resource
from movie.utils.auth_util import generate_token, pw_encode, \
                                  correct_email_format, \
                                  username_format_valid, username_is_unique, \
                                  email_exits, correct_password_format, generateOTP, \
                                  send_email, code_is_correct, get_user, password_is_correct, user_is_admin, check_auth
from movie import db, redis_cli 
from .api_models import AuthNS, AdminNS
import uuid


auth_ns = AuthNS.auth_ns
admin_ns = AdminNS.admin_ns

#--------------------REGISTER LOGIN LOGOUT--------------------
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
      return {"message": "Email format not correct"}, 400

    # check email has been registed or not
    if email_exits(email):
      return {"message": "The email is already been registed"}, 400

    # check user name format
    if not username_format_valid(name):
      return {"message": "Username must be 6-20 characters"}, 400
  
    # check user name has exist or not
    if not username_is_unique(name):
      return {"message": "The username already exists"}, 400

    # check password format
    if not correct_password_format(pw):
      return {"message": "The password is too short, at least 8 characters"}, 400

    #encode pw
    data['id'] = str(uuid.uuid4())

    print(data['id'])
    data['password'] = pw_encode(pw)
    # commit into db
    new_user = User.Users(data)
    db.session.add(new_user)
    db.session.commit()
    print(new_user)

    # generate token, save to redis
    #token = generate_token(email)
    #print(token)
    #redis_cli.set(email, token)

    return {"message": "Successfully registered"}, 200




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
      return {"message": "Please enter correct email"}, 400

    curr_user = get_user(email, is_admin)
    # check the user is valid or not
    if curr_user == None:
      return {"message": "The user not registered"}, 400
      
    # check the user has login or not
    if redis_cli.get(email) != None:
      print(redis_cli.get(email))
      return {"message": "The user has logined"}, 400

    curr_user = get_user(email, is_admin)
    # check the user is valid or not
    if curr_user == None:
      return {"message": "The user not registered"}, 400
    
    if password_is_correct(curr_user, pw):
      return {"message": "Wrong password"}, 400

    token = generate_token(email)
    redis_cli.set(email, token)
    print(token)

    return {
        'id': curr_user.id,
        'token': token,
        'name': curr_user.name
    }, 200
  


  
@auth_ns.route('/logout')
class logoutController(Resource):
  @auth_ns.response(200, "Logout successfullly")
  @auth_ns.response(400, "Something wrong")
  @auth_ns.expect(AuthNS.auth_logout, validate=True)
  def post(self):
    data = auth_ns.payload

    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400

    redis_cli.delete(data['email'])
    return {"message": "logout successfully"}, 200


#-----------------RESET/FORGOT PASSWORD-----------------
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
      return {"message": "Email format not correct"}, 400

    # send vertification code
    code = str(generateOTP())
    try:
      send_email(email, code)
    except:
      return {"message": "Send email failed, try again pls"}, 400

    # update validation code
    user = db.session.query(User.Users).filter(User.Users.email == email).first()
    user.validation_code = code
    db.session.commit()
    return {"message": "code has been send"}, 200

@auth_ns.route('/reset_password')
class ResetPasswordController(Resource):
  @auth_ns.response(200, "Password reset")
  @auth_ns.response(400, "Something wrong")
  @auth_ns.expect(AuthNS.auth_reset_password, validate=True)
  def post(self):
    data = auth_ns.payload
    email = data['email']
    code = data['validation_code']
    new_pw = data['new_password']

    # check the user old password
    user = db.session.query(User.Users).filter(User.Users.email == email).first()
    if user == None:
      return {"message": "Invalid user"}, 400
      
    # check the validation code
    if not code_is_correct(user, code):
      return {"message": "Incorrect validation code"}, 400

    # check password format
    if not correct_password_format(new_pw):
      return {"message": "The password is too short, at least 8 characters"}, 400

    # encode pw
    data['new_password'] = pw_encode(new_pw)

    # update db
    user.password = data['new_password']
    db.session.commit()

    return {"message": "Password updated"}, 200

@auth_ns.route('/forgot_password')
class ForgotPassword(Resource):
  @auth_ns.response(200, "Logout successfullly")
  @auth_ns.response(400, "Something wrong")
  @auth_ns.expect(AuthNS.auth_forgot_password, validate=True)
  def post(self):
    data = auth_ns.payload
    email = data['email']
    pw = data['new_password']
    code = data['validation_code']
    confirm_new_pw = data['confirm_new_password']

    # check email format
    if not correct_email_format(email):
      return {"message": "Email format not correct"}, 400

    # check is admin
    if user_is_admin(email):
      return {"message": "User is admin"}, 400

    # check email exist
    if not email_exits(email):
      return {"message": "The email not exist"}, 400

    # check password format
    if not correct_password_format(pw):
      return {"message": "The password is too short, at least 8 characters"}, 400 

    #check double check pw == pw
    if pw != confirm_new_pw:
      return {"message": "New passwords are not the same"}, 400

    # encode pw
    pw = pw_encode(pw)
    # update db
    user = db.session.query(User.Users).filter(User.Users.email == email).first()

    # check the validation code
    if not code_is_correct(user, code):
      return {"message": "Incorrect validation code"}, 400

    user.password = pw
    db.session.commit()    
    return {"message": "Password updated"}, 200
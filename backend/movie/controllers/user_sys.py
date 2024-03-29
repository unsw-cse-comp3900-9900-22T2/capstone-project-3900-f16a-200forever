from movie.utils.auth_util import username_is_unique, username_format_valid, correct_password_format, pw_encode
from movie.models import user as User
from flask_restx import Resource, reqparse
from movie import db
from movie.utils.other_util import convert_model_to_dict, convert_object_to_dict, paging
from movie.utils.auth_util import   check_auth
from movie import db
from .api_models import UserNS
from movie.utils.other_util import convert_model_to_dict, convert_object_to_dict
from movie.utils.user_util import get_wishlist, get_watchedlist, get_droppedlist, get_badges,  current_username, get_user_id, get_image

user_ns = UserNS.user_ns

#--------------------EVENT-------------------
@user_ns.route("/events")
class UserEvent(Resource):
  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, location='args', required=True)
    args = parser.parse_args()
    email = args['email']

    # 1. check if user_id is valid
    user = db.session.query(User.Users).filter(User.Users.email == email).first()
    if user == None:
      return {"message": "the user not exist"},400

    return {"events": convert_model_to_dict(user.events)}, 200
    
#--------------------PROFILE-------------------
# user profile page
@user_ns.route('/userprofile')
class UserProfileController(Resource):
  @user_ns.response(200, "User profile success")
  @user_ns.response(400, "Something wrong")
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, required=True, location="args")
    args = parser.parse_args()
    user_id = args['user_id']

    this_user = db.session.query(User.Users).filter(User.Users.id == user_id).first()
    if this_user == None:
      return {"message": "User doesn\'t exist"}, 400

    username = this_user.name
    profile_picture = this_user.image
    signature = this_user.signature
    wishlist = get_wishlist(user_id)
    watchedlist = get_watchedlist(user_id)
    droppedlist = get_droppedlist(user_id)
    badges = get_badges(user_id)

    # id, username, profile picture, signature, wishlist, watchlist, droplist, badges
    image = get_image(profile_picture)
    
    user_profile = {
      'id': user_id, #str
      'username': username, #str
      'profile_picture': image, #str
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
    user_id = args['user_id']
    data = user_ns.payload
    email = data['email']
    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400

    # check if user_id is valid
    this_user = db.session.query(User.Users).filter(User.Users.id == user_id).first()
    if this_user == None:
      return {"message": "User doesn\'t exist"}, 400
    
    # check if user has permission to edit
    if this_user.email != email:
      return {"message": "No permission"}, 400

    username = data['username']

    # check new username validity
    if not username_format_valid(username):
      return {"message": "Username must be 6-20 characters"}, 400

    if not username_is_unique(username) and not current_username(user_id) == username:
      return {"message": "Username already taken"}, 400

    # edit pw
    if "current_password" in data.keys():
      # incorrect
      if pw_encode(data['current_password']) != this_user.password:
        return {"message": "Incorrect password"}, 400

      # correct
      if "double_check" in data.keys() and "new_password" in data.keys():
        if not correct_password_format(data['new_password']):
          return {"message": "password formact not correct"}, 400
        if data['double_check'] != data['new_password']:
          return {"message": "2 passwords are not the same"}, 400
        this_user.password = pw_encode(data['new_password'])

    this_user.name = username
    # update signature and image if supplied
    if 'signature' in data.keys():
      this_user.signature = data['signature']
    if 'image' in data.keys():
      this_user.image = data['image'].encode()
    db.session.commit()
    return {
        "message": "Edit profile success"
    }, 200

#--------------------FOLLOWLIST-------------------
@user_ns.route("/followlist")
class FollowListManage(Resource):
  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, location='args', required=True)
    args = parser.parse_args()
    user_id = args['user_id']

    # 1. check the user is valid or not
    user = db.session.query(User.Users).filter(User.Users.id == user_id).first()
    if user == None:
      return {"message": "the user not exist"},400
    
    result = []
    for fo in user.user_follow_list:
      user = fo.follower
      data = {}
      data['email'] = user.email
      data['image'] = get_image(user.image)
      data['id'] = user.id
      data['name'] = user.name
      result.append(data)

    return {"list": result}, 200

  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  @user_ns.expect(UserNS.follow_form, validate=True)
  def post(self):
    data = user_ns.payload
    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400
    
    # check follow valid
    follow = db.session.query(User.Users).filter(User.Users.id == data['follow_id']).first()
    if follow == None:
      return {"message": "User does not exist"}, 400

    # check follow itself
    if data['email'] == follow.email:
      return {"message": "Cannot follow self"}, 400


    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
    
    # check if user in banned list
    banned = db.session.query(User.BannedList).filter(User.BannedList.user_id == user.id, User.BannedList.banned_user_id == data['follow_id']).first()
    if banned != None:
      return {'message': 'Cannot add banned to follow list'}, 400
    
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
  @user_ns.expect(UserNS.follow_form, validate=True)
  def delete(self):
    data = user_ns.payload
    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400

    # check follow valid
    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()

    follow_rel = db.session.query(User.FollowList).filter(User.FollowList.user_id == user.id, User.FollowList.follow_id == data['follow_id']).first()
    if follow_rel == None:
      return {"message": "Haven't followed before"}, 400

    db.session.delete(follow_rel)
    db.session.commit()
    return {"message": "Successfully"}, 200

@user_ns.route("/followlist/reviews")
class FollowReview(Resource):
  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  @user_ns.expect(UserNS.follow_form, validate=True)
  def post(self):
    data = user_ns.payload
    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400
      
    if "page_num" not in data.keys() or "num_per_page" not in data.keys():
      return {"message": "page_num and num_per_page should by provided, type are both int"}, 400

    # check the user in the follow list
    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
    if user == None:
      return {'message': "invalid user email"}, 400

    follow = db.session.query(User.Users).filter(User.Users.id == data['follow_id']).first()
    if follow == None:
      return {"message": "Haven't followed"}, 400

    follow_rel = db.session.query(User.FollowList).filter(User.FollowList.user_id == user.id, User.FollowList.follow_id == follow.id).first()
    if follow_rel == None:
      return {"message": "Haven't followed before"}, 400

    # get the reviews 
    result = follow.reviews
    result = paging(data['page_num'], data['num_per_page'], result)
    reviews = []
    for re in result:
      review = convert_object_to_dict(re)
      review["review_id"] = review.pop("id")
      movie = convert_object_to_dict(re.movies)
      review.update(movie)
      review["user_email"] = re.user.email
      review['user_id'] = re.user.id
      review["user_image"] = get_image(re.user.image)
      reviews.append(review)

    reviews.sort(key=lambda x: x["created_time"])
    reviews.reverse()
    # print(reviews)
    
    return {"reviews": reviews}, 200

#--------------------BANNEDLIST-------------------
@user_ns.route('/bannedlist')
class BannedlistController(Resource):
  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, location='args', required=True)
    args = parser.parse_args()
    user_id = args['user_id']

    # 1. check the user is valid or not
    user = db.session.query(User.Users).filter(User.Users.id == user_id).first()
    if user == None:
      return {"message": "user does not exist"},400
    
    result = []
    for ban in user.user_banned_list:
      user = ban.banner
      data = {}
      data['email'] = user.email
      data['image'] = get_image(user.image)
      data['id'] = user.id
      data['name'] = user.name
      result.append(data)

    return {"list": result}, 200

  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  @user_ns.expect(UserNS.banned_form, validate=True)
  def post(self):
    data = user_ns.payload

    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400

    banned_id = data['banned_id']
    # check ban valid
    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
    if user == None:
      return {"message": "User does not exist"}, 400

    banned = db.session.query(User.Users).filter(User.Users.id == banned_id).first()
    if banned == None:
      return {"message": "Banned user dose not exist"}, 400

    # check ban itself
    if data['email'] == banned.email:
      return {"message": "Cannot ban self"}, 400

    # check if user already in banned list
    banned = db.session.query(User.BannedList).filter(User.BannedList.user_id == user.id, User.BannedList.banned_user_id == banned_id).first()
    if banned != None:
      return {'message': 'User already in banned list'}, 400

    # check if user in follow list
    follow = db.session.query(User.FollowList).filter(User.FollowList.user_id == user.id, User.FollowList.follow_id == banned_id).first()
    if follow != None:
      return {'message': 'Cannot add followed to ban list'}, 400

    data['user_id'] = user.id
    data['banned_user_id'] = banned_id
    entry = User.BannedList(data)
    db.session.add(entry)
    db.session.commit()

    return {"message": "Successfully"}, 200

  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  @user_ns.expect(UserNS.banned_form, validate=True)
  def delete(self):
    data = user_ns.payload
    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400

    # check ban valid
    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
    if user == None:
      return {"message": "User does not exist"}, 400

    banned = db.session.query(User.Users).filter(User.Users.id == data['banned_id']).first()
    if banned == None:
      return {"message": "Banned user does not exist"}, 400
    
    banned = db.session.query(User.BannedList).filter(User.BannedList.user_id == user.id, User.BannedList.banned_user_id == banned.id).first()
    if banned == None:
      return {"message": "Haven't banned before"}, 400

    db.session.delete(banned)
    db.session.commit()
    return {"message": "Successfully"}, 200

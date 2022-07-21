
import imp
from movie.controllers.api_models import ThreadNS
from flask_restx import Resource, reqparse
from flask import session
from movie.utils.auth_util import user_has_login, user_is_valid
from movie.models import thread as Thread
from movie.models import user as User
from movie.models import admin as Admin
from movie.models import genre as Genre
from movie import db
import uuid
from datetime import datetime
from movie.utils.other_until import convert_model_to_dict
from movie.utils.user_util import get_user_id

thread_ns = ThreadNS.thread_ns

@thread_ns.route('')
class ThreadManager(Resource):
  @thread_ns.response(200, "Successfully")
  @thread_ns.response(400, 'Something went wrong')
  @thread_ns.expect(ThreadNS.delete_thread_form, validate=True)
  def delete(self):
    data = thread_ns.payload
    """
    # login
    if not user_has_login(data['email'], session):
      return {"message": "the user has not logined"}, 400

    # valid token
    if not user_is_valid(data):
      return {"message": "the token is incorrect"}, 400
    """


    # thread exist
    thread = db.session.query(Thread.Threads).filter(Thread.Threads.id == data['thread_id']).first()
    if thread == None:
      return {'message': 'The thread not exist'}, 400

    # thread own by the user
    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
    admin = None
    if user == None:
      admin = db.session.query(Admin.Admins).filter(Admin.Admins.email == data['email']).first()
   
    if user != None and thread.user_id != user.id and user.is_forum_admin != 1:
      return {"message": 'No permission'}, 400

    if user == None and admin == None:
      return {"message": 'No permission'}, 400
    
    # delete the thread
    db.session.delete(thread)
    db.session.commit()
    return {"message": 'Delete thread successfully'}, 200

  @thread_ns.response(200, "Successfully")
  @thread_ns.response(400, 'Something went wrong')
  @thread_ns.expect(ThreadNS.post_thread_form, validate=True)
  def post(self):
    data = thread_ns.payload
    data['created_time'] = str(datetime.now())
    """
    # check user login
    if not user_has_login(data['email'], session):
      return {"message": "the user has not logined"}, 400

    # check user valid
    if not user_is_valid(data):
      return {"message": "the token is incorrect"}, 400
    """


    # check genre valid
    genre = db.session.query(Genre.Genres).filter(Genre.Genres.id == data['genre_id']).first()
    if genre == None:
      return {"message": "Genre id invalid"}, 400
    
    # check is_anonymous
    if data['is_anonymous'] != 0 and data['is_anonymous'] != 1:
      return {"message": "Invalid is_anonymous value"}, 400

    # post
    data['user_id'] = get_user_id(data['email'])
    data['id'] = str(uuid.uuid4())
    thread = Thread.Threads(data)
    db.session.add(thread)
    db.session.commit()
    return {"thread_id": data['id']}, 200


@thread_ns.route('/admin')
class ThreadAdmin(Resource):
  @thread_ns.response(200, "Successfully")
  @thread_ns.response(400, 'Something went wrong')
  @thread_ns.expect(ThreadNS.forum_admin_form, validate=True)
  def post(self):
    data = thread_ns.payload
    """
    # check admin has login
    if not user_has_login(data['admin_email'], session):
      return {"message": "the user has not logined"}, 400

    # check admin valid
    data['email'] = data['admin_email']
    if not user_is_valid(data):
      return {"message": "the token is incorrect"}, 400
    """


    # check is admin
    admin = db.session.query(Admin.Admins).filter(Admin.Admins.email == data['admin_email']).first()
    if admin == None:
      return {"message": "No permission"}, 400

    # check user valid
    user = db.session.query(User.Users).filter(User.Users.email == data['user_email']).first()
    if user == None:
      return {"message": "The user not exist"}, 400

    # check user has already be a admin
    if user.is_forum_admin == 1:
      return {"message": "The user is already a forum admin"}, 400

    # update to admin
    user.is_forum_admin = 1
    db.session.commit()
    return {'message': "Successfully"}, 200

"""
@thread_ns.route('/categories')
class ThreadAdmin(Resource):
  @thread_ns.response(200, "Successfully")
  @thread_ns.response(400, 'Something went wrong')
  @thread_ns.expect(ThreadNS.forum_admin_form, validate=True)
  def get(self):
    categories = db.session.query(Thread.Categories).all()
    categories = convert_model_to_dict(categories)
    return {"categories": categories}, 200
"""

@thread_ns.route('/react')
class ReactToComment(Resource):
  @thread_ns.response(200, "Successfully")
  @thread_ns.response(400, 'Something went wrong')
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, location = 'args', required=True)
    parser.add_argument('comment_id', type=str, location = 'args', required=True)
    args = parser.parse_args()
    comment_id = args['comment_id']
    user_id = args['user_id']
    data = {'user_id': user_id, 'comment_id': comment_id}
    new_comment_reaction = Thread.CommentLikes(data)
    db.session.add(new_comment_reaction)
    db.session.commit()

    return {"message": "Reaction add successfully"}, 200


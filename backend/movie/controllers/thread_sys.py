from movie.controllers.api_models import ThreadNS
from flask_restx import Resource, reqparse
from flask import session
from movie.utils.auth_util import  check_auth
from movie.models import thread as Thread
from movie.models import user as User
from movie.models import admin as Admin
from movie.models import genre as Genre
from movie import db
import uuid
from datetime import datetime
from movie.utils.other_util import paging, convert_object_to_dict
from movie.utils.user_util import get_user_id, get_image

thread_ns = ThreadNS.thread_ns

#----------------GET ALL THREADS------------------
@thread_ns.route('')
class ThreadManager(Resource):
  @thread_ns.response(200, "Successfully")
  @thread_ns.response(400, 'Something went wrong')
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('genre_id', type=str, required=True, location="args")
    parser.add_argument('num_per_page', type=int, location='args')
    parser.add_argument('page', type=int, location='args')
    args = parser.parse_args()

    # check valid genre id
    genre = db.session.query(Genre.Genres).filter(Genre.Genres.id == args['genre_id']).first()
    if genre == None:
      return {"message": "Genre id invalid"}, 400

    # default the first page is 1
    if args['page'] == None:
      args['page'] = 1

    # default num of threads in one page is 10
    if args['num_per_page'] == None:
      args['num_per_page'] = 10

    threads = db.session.query(Thread.Threads).filter(Thread.Threads.genre_id == args['genre_id']).order_by(Thread.Threads.created_time.desc()).all()
    num_threads = len(threads)
    threads = paging(args['page'], args['num_per_page'], threads)
    thread_result =[]
    for thread in threads:
      tmp = convert_object_to_dict(thread)
      tmp["react_num"] = len(thread.thread_likes)
      tmp["user_email"] = thread.user.email
      tmp["user_image"] = get_image(thread.user.image)
      thread_result.append(tmp)

    return {"threads": thread_result, "num_threads": num_threads}, 200


#----------------Thread Manager------------------
@thread_ns.route('/thread')
class ThreadController(Resource):
  @thread_ns.response(200, "Successfully")
  @thread_ns.response(400, 'Something went wrong')
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('thread_id', type=str, required=True, location="args")
    parser.add_argument('num_per_page', type=int, location='args')
    parser.add_argument('page', type=int, location='args')
    args = parser.parse_args()

    # check valid genre id
    thread = db.session.query(Thread.Threads).filter(Thread.Threads.id == args['thread_id']).first()
    if thread == None:
      return {"message": "Thread id invalid"}, 400

    # default the first page is 1
    if args['page'] == None:
      args['page'] = 1

    # default num of comments in one page is 10
    if args['num_per_page'] == None:
      args['num_per_page'] = 10

    comments = db.session.query(Thread.ThreadComment).filter(Thread.ThreadComment.thread_id == args['thread_id']).order_by(Thread.ThreadComment.comment_time.desc()).all()
    num_comments = len(comments)
    comments = paging(args['page'], args['num_per_page'], comments)
    
    # get thread data
    thread_data = convert_object_to_dict(thread)
    thread_data["react_num"] = len(thread.thread_likes)
    thread_data["user_email"] = thread.user.email
    thread_data["user_image"] = get_image(thread.user.image)

    # get comment
    comment_data = []
    for co in comments:
      tmp = convert_object_to_dict(co)
      tmp["user_email"] = co.user.email
      tmp["user_image"] = get_image(co.user.image)
      comment_data.append(tmp)

    return {"thread": thread_data, "comments": comment_data, "num_comments": num_comments}, 200

  @thread_ns.response(200, "Successfully")
  @thread_ns.response(400, 'Something went wrong')
  @thread_ns.expect(ThreadNS.delete_thread_form, validate=True)
  def delete(self):
    data = thread_ns.payload
    # check auth
    message, auth_correct = check_auth(data["email"], data['token'])

    if not auth_correct:
      return {"message": message}, 400

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
    # check auth
    message, auth_correct = check_auth(data["email"], data['token'])

    if not auth_correct:
      return {"message": message}, 400

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


#----------------MANAGE THREAD ADMIN-----------------
@thread_ns.route('/admin')
class ThreadAdmin(Resource):
  @thread_ns.response(200, "Successfully")
  @thread_ns.response(400, 'Something went wrong')
  @thread_ns.expect(ThreadNS.forum_admin_form, validate=True)
  def put(self):
    data = thread_ns.payload
    # check auth
    message, auth_correct = check_auth(data["admin_email"], data['token'])
    if not auth_correct:
      return {"message": message}, 400

    # check is admin
    admin = db.session.query(Admin.Admins).filter(Admin.Admins.email == data['admin_email']).first()
    if admin == None:
      return {"message": "No permission"}, 400

    # check user valid
    user = db.session.query(User.Users).filter(User.Users.email == data['user_email']).first()
    if user == None:
      return {"message": "The user not exist"}, 400

    # promoting
    if data['become_admin'] == True:
      # check if user is already a forum admin
      if user.is_forum_admin == 1:
        return {"message": "The user is already a forum admin"}, 400
      else:
        # update to admin
        user.is_forum_admin = 1
    # demoting
    else:
      # check if user is already a forum admin
      if user.is_forum_admin == 0:
        return {"message": "The user is not a forum admin"}, 400
      else:
        # demote from admin
        user.is_forum_admin = 0

    db.session.commit()
    return {"message": "Successfully"}, 200


#----------------REACT THREAD-----------------
@thread_ns.route('/react')
class ReactToComment(Resource):
  @thread_ns.response(200, "Successfully")
  @thread_ns.response(400, 'Something went wrong')
  @thread_ns.expect(ThreadNS.thread_react_form, validate=True)
  def post(self):
    data = thread_ns.payload
    # check auth
    message, auth_correct = check_auth(data["email"], data['token'])

    if not auth_correct:
      return {"message": str(message)}, 400

    # check user valid
    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
    if user == None:
      return {"message": "Incalid user"}, 400
    # check comment valid
    comment = db.session.query(Thread.Threads).filter(Thread.Threads.id == data['thread_id']).first()
    if comment == None:
      return {"message": "Thread not exist"}, 400

    react = db.session.query(Thread.ThreadLikes).filter(Thread.ThreadLikes.thread_id == data['thread_id'], Thread.ThreadLikes.user_id == user.id).first()
    if react == None:
      new_react = Thread.ThreadLikes({'user_id': user.id, 'thread_id': data['thread_id']})
      db.session.add(new_react)
      db.session.commit()
      return {"is_remove": 1}, 200
    else:
      db.session.delete(react)
      db.session.commit()
      return {"is_remove": 0}, 200

#----------------COMMENT----------------
@thread_ns.route('/comment')
class CommentThread(Resource):
  @thread_ns.response(200, "Successfully")
  @thread_ns.response(400, 'Something went wrong')
  @thread_ns.expect(ThreadNS.thread_comment_form, validate=True)
  def post(self):
    data = thread_ns.payload

    now = datetime.now()
    data['time'] = now
    # check auth
    message, auth_correct = check_auth(data["email"], data['token'])

    if not auth_correct:
      return {"message": message}, 400
    # check user valid
    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
    if user == None:
      return {"message": "Invalid user"}, 400

    # check thread id
    thread = db.session.query(Thread.Threads).filter(Thread.Threads.id == data['thread_id']).first()
    if thread == None:
      return {"message": "Thread Not Exist"},400

    # check reply comment id
    if 'reply_comment_id' in data.keys():
      parent = db.session.query(Thread.ThreadComment).filter(Thread.ThreadComment.id == data['reply_comment_id']).first()
      if parent == None or parent.thread_id != thread.id:
        return {"message":"Parent id invalid"}, 400

    data['user_id'] = user.id
    data['id'] = str(uuid.uuid4())
    comment = Thread.ThreadComment(data)
    db.session.add(comment)
    db.session.commit()
    return {"comment_id": data['id']}, 200

  @thread_ns.response(200, "Successfully")
  @thread_ns.response(400, 'Something went wrong')
  @thread_ns.expect(ThreadNS.thread_comment_form, validate=True)
  def delete(self):
    data = thread_ns.payload
    # check auth
    message, auth_correct = check_auth(data["email"], data['token'])

    if not auth_correct:
      return {"message": str(message)}, 400
    # check user valid
    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
    if user == None:
      return {"message": "Invalid user"}, 400
    # check comment valid
    comment = db.session.query(Thread.ThreadComment).filter(Thread.ThreadComment.id == data['comment_id']).first()
    if comment == None:
      return {"message": "Comment not exist"}, 400

    # check comment belongs to user
    if comment.user_id != user.id:
      return {"message": "You can't delete this comment"}, 400

    # delete comment
    db.session.delete(comment)
    db.session.commit()
    return {"message": "Successfully"}, 200


    





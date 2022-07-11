from concurrent.futures import thread
from movie.controllers.api_models import ThreadNS
from flask_restx import Resource, reqparse
from flask import session
from movie.utils.auth_util import user_has_login, user_is_valid
from movie.models import thread as Thread
from movie import db

thread_ns = ThreadNS.thread_ns

@thread_ns.route('')
class ThreadManager(Resource):
  @thread_ns.response(200, "Successfully")
  @thread_ns.response(400, 'Something went wrong')
  @thread_ns.expect(ThreadNS.delete_thread_form, validate=True)
  def delete(self):
    data = thread_ns.payload

    # login
    if not user_has_login(data['email'], session):
      return {"message": "the user has not logined"}, 400

    # valid token
    if not user_is_valid(data):
      return {"message": "the token is incorrect"}, 400

    # thread exist
    thread = db.session.query(Thread.Threads).filter(Thread.Threads.id == data['thread_id']).first()
    if thread == None:
      return {'message': 'The thread not exist'}, 400

    # thread own by the user
    user_id = session[data['email']]['id']
    if thread.user_id != user_id:
      return {"message": 'No permission'}, 400
    
    # delete the thread
    db.session.delete(thread)
    db.session.commit()
    return {"message": 'Delete thread successfully'}, 200
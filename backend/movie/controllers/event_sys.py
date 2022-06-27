
from datetime import datetime
from json import dumps
from attr import validate
from flask_restx import Resource, reqparse
import datetime
from movie.models import event as Event
from numpy import require

from movie.utils.auth_util import user_is_valid, user_is_admin, check_correct_answer
from .api_models import EventNS
import uuid
from movie import db
from flask import session

event_ns = EventNS.event_ns

@event_ns.route('/create')
class EventCreate(Resource):
  @event_ns.response(200, "Create Event Successfully")
  @event_ns.response(400, "TODO")
  @event_ns.expect(EventNS.event_create_form, validate=True)
  def post(self):
    data = event_ns.payload
    email = data['email']
    token = data['token']

    # check the user is valid or not
    if not user_is_valid(email, token):
      return dumps({"message": "the token is incorrect"}), 400
    
    # check the user is admin
    if not user_is_admin(email):
      return dumps({"message": "the user is admin, not permission"}), 400

    event = event_ns.payload
    del event['email']
    del event['token']
    event_id = uuid.uuid4()

    questions = event['questions']
    del event['questions']
    event['id'] = event_id
    event['admin_id'] = session['id']
    for que in list(questions):
      que = dict(que)
      if not check_correct_answer(int(que['correct_answer'])):
        return {'message': 'correct_answer must be 1 or 2 or 3'}, 400
      que_id = uuid.uuid4()
      que['id'] = que_id
      que['event_id'] = event['id']
      new_que = Event.Questions(que)
      db.session.add(new_que)
      db.session.commit()
    new_event  = Event.Events(event)
    db.session.add(new_event)
    db.session.commit()

    return dumps({"message": "Create Event Successfully"}), 200




from datetime import datetime
from flask_restx import Resource, reqparse
import datetime
from movie.models import event
from numpy import require
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
    event = event_ns.payload
    event_id = uuid.uuid4()

    questions = event['questions']
    del event['questions']
    event['id'] = event_id
    event['admin_id'] = 1#session['id']
    for que in list(questions):
      que = dict(que)
      if not check_correct_answer(int(que['correct_answer'])):
        return {'message': 'correct_answer must be 1 or 2 or 3'}, 400
      que_id = uuid.uuid4()
      que['id'] = que_id
      que['event_id'] = event['id']
      new_que = event.Questions(que)
      db.session.add(new_que)
      db.session.commit()
    new_event  = event.Events(event)
    db.session.add(new_event)
    db.session.commit()




def check_correct_answer(value):
  if value != 1 and value != 2 and value != 3:
    return False
  return True
    
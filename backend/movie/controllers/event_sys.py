
from datetime import datetime
from flask_restx import Resource, reqparse
from datetime import datetime
from movie.models import user as User
from movie.models import event as Event
from movie.models import movie as Movie
from fuzzywuzzy import process
from movie.utils.auth_util import user_is_admin, check_auth
from movie.utils.movie_util import format_movie_return_list
from movie.utils.other_util import  convert_object_to_dict
from movie.utils.event_util import create_event
from movie.utils.user_util import  get_user_id, get_image
from .api_models import EventNS
import uuid
from movie import db


event_ns = EventNS.event_ns

#--------------------GET EVENT LIST--------------------
@event_ns.route('')
class GetAllEvents(Resource):
  @event_ns.response(200, "Successfully")
  @event_ns.response(400, "Something wrong")
  def get(self):
    events = db.session.query(Event.Events).filter(Event.Events.event_status == 'open').all()
    result = []
    for event in events:
      tmp = convert_object_to_dict(event)
      tmp['image'] = get_image(tmp['image'])
      result.append(tmp)
    return {"events": result}, 200

#--------------------GET EVENT DETAIL--------------------
@event_ns.route('/detail')
class GetEventDetail(Resource):
  @event_ns.response(200, "Successfully")
  @event_ns.response(400, "Something wrong")
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str, location='args', required=True)
    args = parser.parse_args()
    id = args['id']
    event = db.session.query(Event.Events).filter(Event.Events.id == id).first()

    if event == None:
      return {"message": f'Event {id} not found'}, 400
    
    data = convert_object_to_dict(event)
    data['image'] = get_image(data['image'])
    questions = {}
    for que in event.questions:
      questions[que.content] = [que.choice_1, que.choice_2, que.choice_3]
    data["questions"] = questions
    return data, 200

#--------------------MANAGE EVENT--------------------
@event_ns.route('/create')
class EventCreate(Resource):
  @event_ns.response(200, "Create Event Successfully")
  @event_ns.response(400, "Something wrong")
  @event_ns.expect(EventNS.event_create_form, validate=True)
  def post(self):
    data = event_ns.payload

    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400

    # check the user is admin
    if not user_is_admin(data['email']):
      return {"message": "the user is not the admin, no permission"}, 400

    event_id = str(uuid.uuid4())
    # add event
    if not create_event(event_id, data):
      return {"message": "Create Event Failed"}, 400
    return {"message": "Create Event Successfully"}, 200

@event_ns.route("/search")
class Search(Resource):
  @event_ns.response(200, "Search successfully")
  @event_ns.response(400, "Something wrong")
  def get(self):   
    parser = reqparse.RequestParser()
    parser.add_argument('keyword', type=str, location='args', required=True)
    args = parser.parse_args()
    kw = args['keyword']

    # check empty string
    if kw == '':
      return {"message": "Please do not enter empty string"}, 400
    # get all the match results
    matched_movies = db.session.query(Movie.Movies).filter(Movie.Movies.title.ilike(f'%{kw}%')).all()
    # get the best match use fuzzywuzzy
    best = process.extract(kw, matched_movies, limit=15)

    movies = format_movie_return_list(best)

    return {"result": movies}, 200

@event_ns.route('/edit')
class EditEvent(Resource):
  @event_ns.response(200, "Successfully")
  @event_ns.response(400, "Something wrong")
  @event_ns.expect(EventNS.event_edit_form, validate=True)
  def put(self):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str, location='args', required=True)
    args = parser.parse_args()
    id = args['id']
    data = event_ns.payload
 
    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400

    # check the user is admin
    if not user_is_admin(data['email']):
      return {"message": "the user is not the admin, no permission"}, 400
      
    # get the id
    event = db.session.query(Event.Events).filter(Event.Events.id == id).first()
    if event == None:
      return {"message": "The event not found"}, 400
    
    try:
      # detele question
      db.session.query(Event.Questions).filter(Event.Questions.event_id == id).delete()
      # delete movie
      db.session.query(Event.EventMovie).filter(Event.EventMovie.event_id == id).delete()
      # delet event
      db.session.delete(event)
      db.session.flush()

      if not create_event(id, data):
        raise
      db.session.commit()
    except:
      db.session.rollback()

      return {"message": "Update false"}, 400
    return {"message": "Updated"}, 200
  
#--------------------ATTEMP EVENT--------------------
@event_ns.route('/attemp')
class AttempEvent(Resource):
  @event_ns.response(200, "Successfully")
  @event_ns.response(400, "Something wrong")
  @event_ns.expect(EventNS.attemp_event_form, validate=True)
  def post(self):
    now = datetime.now()
    data = event_ns.payload
 
    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400

    # check event valid
    event = db.session.query(Event.Events).filter(Event.Events.id == data['event_id']).first()
    if event == None:
      return {"message": "Event not exists"}, 400

    # attemp the event
    user_id = get_user_id(data['email'])
    if user_id == None:
      return {"message": "user does not exist"}, 400

    data['user_id'] = user_id
    data['start_time'] = now
    new = User.UserEvent(data)
    try:
      db.session.add(new)
      db.session.commit()
    except:
      db.session.rollback()
      return {"message": "cannot enter twice"}, 400

    return {"message": "sucessfull"}, 200

@event_ns.route('/finish')
class AttempEvent(Resource):
  @event_ns.response(200, "Successfully")
  @event_ns.response(400, "Something wrong")
  @event_ns.expect(EventNS.finish_event_form, validate=True)
  def post(self):
    now = datetime.now()
    data = event_ns.payload
 
    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400
    event = db.session.query(Event.Events).filter(Event.Events.id == data['event_id']).first()
    if event == None:
      return {"message": "The event not exists"}, 400
    duration = event.duration
    user_id = get_user_id(data['email'])
    if user_id == None:
      return {"message": "user does not exist"}, 400

    # check the user have attemped the event or not
    event_attemp = db.session.query(User.UserEvent).filter(User.UserEvent.event_id == data['event_id'], \
      User.UserEvent.user_id == user_id).first()
    if event_attemp == None:
      return {"message": "The user haven't attemp the event before"}, 400

    # check the status
    if event_attemp.event_status != 'attemping':
      return {"message": "Have finished the event"}, 400

    # check the time 
    diff = (now - event_attemp.start_time).seconds
    print(duration*60)
    if diff > duration*60:
      # update the db
      event_attemp.end_time = now
      event_attemp.event_status = 'failed'
      db.session.commit()
      return {"message": "Time out"}, 400

    # check the answer
    questions = event.questions
    answers = data['answers']
    num = 0
    correctness = 0
    if len(questions) != len(answers.keys()):
      # update the db
      event_attemp.end_time = now
      event_attemp.event_status = 'failed'
      db.session.commit()
      return {"message": "Failed"}, 400

    for que in questions:
      # check the answer
      if que.id not in answers.keys():
        return {"message":"Answer id is invalid"}, 400
      if que.correct_answer == int(answers[que.id]):
        correctness+=1
      num+=1
    if correctness < event.require_correctness_amt:
      # update the db
      event_attemp.end_time = now
      event_attemp.event_status = 'failed'
      db.session.commit()
      return {"result": "Failed", "correctness": correctness, "require": event.require_correctness_amt}, 200

    # user get the event
    event_attemp.end_time = now
    event_attemp.event_status = 'passed'
    db.session.commit()
    return {"correctness": correctness, 'result': 'Pass', "require": event.require_correctness_amt}, 200

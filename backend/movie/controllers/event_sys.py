
from datetime import datetime
from json import dumps
from attr import validate
from flask_restx import Resource, reqparse
import datetime
from movie.models import event as Event
from movie.models import movie as Movie
from numpy import require
from fuzzywuzzy import process
from movie.utils.auth_util import user_is_valid, user_is_admin, check_correct_answer, user_has_login
from movie.utils.movie_until import movie_id_valid
from .api_models import EventNS
import uuid
from movie import db
from flask import session

event_ns = EventNS.event_ns

@event_ns.route('/create')
class EventCreate(Resource):
  @event_ns.response(200, "Create Event Successfully")
  @event_ns.response(400, "Something wrong")
  @event_ns.expect(EventNS.event_create_form, validate=True)
  def post(self):
    data = event_ns.payload

    if not user_has_login(data['email'], session):
      return {"message": "the user has not logined"}, 400

    # check the user is valid or not
    if not user_is_valid(data):
      return dumps({"message": "the token is incorrect"}), 400
    
    # check the user is admin
    if not user_is_admin(data['email']):
      return dumps({"message": "the user is not the admin, no permission"}), 400

    event = event_ns.payload
    event_id = uuid.uuid4()
    # add event
    try:
      event['id'] = event_id
      admin_id = session[data['email']]["id"]
      event['admin_id'] = admin_id
      new_event  = Event.Events(event)
      db.session.add(new_event)
      db.session.flush()

      # add question
      questions = event['questions']
      del event['questions']

      for que in list(questions):
        que = dict(que)
        if not check_correct_answer(int(que['correct_answer'])):
          return {'message': 'correct_answer must be 1 or 2 or 3'}, 400
        que_id = uuid.uuid4()
        que['id'] = que_id
        que['event_id'] = event['id']
        new_que = Event.Questions(que)
        db.session.add(new_que)
        db.session.flush()
    
        # add movie
      movieid_set = event['movies']
      for movie in list(movieid_set):
        if not movie_id_valid(session, movie):
          raise
        data['movie_id'] = movie
        data['event_id'] = event['id']
        new_rel = Event.EventMovie(data)
        db.session.add(new_rel)
        db.session.flush()
      db.session.commit()
    except:
      db.session.rollback()
      return dumps({"message": "Create Event Failed"}), 400


    return dumps({"message": "Create Event Successfully"}), 200



@event_ns.route("/search")
class Search(Resource):
  @event_ns.response(200, "Login Successfully")
  @event_ns.response(400, "Something wrong")
  @event_ns.expect(EventNS.validation_form, validate=True)
  def post(self):   
    data = event_ns.payload

    # check user has login
    if not user_has_login(data['email'], session):
      return {"message": "the user has not logined"}, 400

    # check the user is valid or not
    if not user_is_valid(data):
      return dumps({"message": "the token is incorrect"}), 400
        # check the user is admin
    if not user_is_admin(data['email']):
      return dumps({"message": "the user is not the admin, no permission"}), 400

    parser = reqparse.RequestParser()
    parser.add_argument('keyword', type=str, location='args', required=True)
    """
    parser.add_argument('description', type=str, location='args', required=True)
    parser.add_argument('genre', type=str, location='args', required=True)
    parser.add_argument('director', type=str, location='args', required=True)
    parser.add_argument('actor', type=str, location='args', required=True)
    """
    args = parser.parse_args()
    kw = args['keyword']

    # check empty string
    if kw == '':
      return dumps({"message": "Please do not enter empty string"}), 400

    # get all the match results
    matched_movies = db.session.query(Movie.Movies).filter(Movie.Movies.title.ilike(f'%{kw}%')).all()
    # get the best match use fuzzywuzzy
    best =  process.extract(kw, matched_movies, limit=15)

    result = []
    for movie in best:
      movie = movie[0]
      data = {}
      data['id'] = movie.id
      data['title'] = movie.title
      data['relese_time'] = movie.release_time.year
      result.append(data)

    return dumps({"result": result}), 200
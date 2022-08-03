from movie import db
from flask import session
from movie.models import event as Event
from movie.models import movie as Movie
from movie.utils.auth_util import  user_is_admin, check_correct_answer
import uuid
from movie.utils.movie_util import movie_id_valid

from movie.utils.user_util import get_admin_id

# Create an event and add it to the database
# Args: event_id (string), event (datbase type)
# Return: Boolean
def create_event(event_id, event):
  try:
    event['id'] = event_id
    admin_id = get_admin_id(event['email'])
    event['admin_id'] = admin_id
    new_event  = Event.Events(event)
    db.session.add(new_event)
    db.session.flush()
    # add question
    questions = event['questions']
    del event['questions']

    # check amount
    if len(questions) < event['require_correctness_amt']: 
      return False
    for que in list(questions):
      que = dict(que)
      if not check_correct_answer(int(que['correct_answer'])):
        print("hi")
        return False
      que_id = str(uuid.uuid4())
      que['id'] = que_id
      que['event_id'] = event['id']
      new_que = Event.Questions(que)
      db.session.add(new_que)
      db.session.flush()
      # add movie
    movieid_set = event['movies']
    for movie in list(movieid_set):
      if not movie_id_valid(movie):
        raise
      event['movie_id'] = movie
      event['event_id'] = event['id']
      new_rel = Event.EventMovie(event)
      db.session.add(new_rel)
      db.session.flush()
    db.session.commit()
  except:
    db.session.rollback()
    return False
  return True
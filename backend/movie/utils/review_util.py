from sqlalchemy import inspect
from movie import db
import movie.models.review as Review
import movie.models.user as User
import movie.models.event as Event

def user_reviewed_movie(user, movie):
  review = db.session.query(Review.Reviews).filter(Review.Reviews.user_id == user).filter(Review.Reviews.movie_id == movie).first()
  print(review)
  if review == None:
    return False
  return True


# weight is 2 if user has badge, 1 otherwise
def calculate_weight(user, movie):
  badges = db.session.query(User.UserEvent).filter(User.UserEvent.user_id == user).filter(User.UserEvent.event_status.like(f'%passed%')).all()
  for badge in badges:
    #print(badge.event_id)
    exists = db.session.query(Event.EventMovie).filter(Event.EventMovie.event_id == badge.event_id).filter(Event.EventMovie.movie_id == movie).first()
    if exists != None:
      return 2
  return 1

# adjust review list for banned list
def adjust_reviews(user_id, review_list):
  banned_list = db.session.query(User.BannedList).filter(User.BannedList.user_id == user_id).all()
  for review in review_list:
    for banned in banned_list:
      if banned.banned_user_id == review[1].id:
        review_list.remove(review)
        continue
  return review_list
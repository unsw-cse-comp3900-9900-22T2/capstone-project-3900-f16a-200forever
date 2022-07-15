from sqlalchemy import inspect
from movie import db
import movie.models.review as Review

def user_reviewed_movie(user, movie):
  review = db.session.query(Review.Reviews).filter(Review.Reviews.user_id == user).filter(Review.Reviews.movie_id == movie).first()
  print(review)
  if review == None:
    return False
  return True

# TODO
def calculate_weight(user, movie):
  return 1
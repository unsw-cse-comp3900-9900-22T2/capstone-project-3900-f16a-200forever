from movie.utils.movie_until import movie_id_valid
from movie.utils.auth_util import user_is_valid, user_has_login
from movie.utils.review_util import user_reviewed_movie, calculate_weight
from movie.utils.user_util import get_user_id
from movie.models import review as Review
from flask_restx import Resource, reqparse
from .api_models import ReviewNS
from json import dumps
from flask import session, jsonify
from movie import db
import datetime
import uuid


review_ns = ReviewNS.review_ns

# user profile page
@review_ns.route('/review')
class ReviewController(Resource):
  @review_ns.response(200, "Create review success")
  @review_ns.response(400, "Something wrong")
  @review_ns.expect(ReviewNS.review_create_form, validate=True)
  def post(self):
    data = review_ns.payload
    email = data['email']
    movie = data['movie_id']
    rating = data['rating']
    user_id = get_user_id(email)


    # check if logged in
    '''if not user_has_login(email, session):
      return {"message": "the user has not logined"}, 400

    # check token
    if not user_is_valid(data):
      return {"message": "Invalid user id"}, 400'''

    # check rating between 1-5
    if rating < 1 or rating > 5:
      return {"message": "Rating should be 1-5"}, 400

    # check valid user and movie ids
    if not movie_id_valid(movie):
      return {"message": "Invalid movie id"}, 400

    # check user hasn't already reviewed this movie
    if user_reviewed_movie(user_id, movie):
      return {"message": "User already reviewed this movie"}, 400

    data['id'] = str(uuid.uuid4())
    data['user_id'] = user_id
    data['created_time'] = datetime.datetime.now()
    data['weight'] = calculate_weight(user_id, movie)

    # commit into db
    new_review = Review.Reviews(data)
    print(new_review)
    db.session.add(new_review)
    db.session.commit()

    return {
        "message": "Create review success"
    }, 200


  @review_ns.response(200, "Delete review success")
  @review_ns.response(400, "Something wrong")
  @review_ns.expect(ReviewNS.review_delete_form, validate=True)
  def delete(self):
    data = review_ns.payload
    email = data['email']
    

    # check if logged in
    '''if not user_has_login(email, session):
      return {"message": "the user has not logined"}, 400

    # check token
    if not user_is_valid(data):
      return {"message": "Invalid user id"}, 400'''

    return {
        "message": "Delete review success"
    }, 200
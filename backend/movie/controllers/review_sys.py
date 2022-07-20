from movie.utils.movie_until import movie_id_valid
from movie.utils.auth_util import user_is_valid, user_has_login
from movie.utils.review_util import user_reviewed_movie, calculate_weight
from movie.utils.user_util import get_user_id
from movie.models import review as Review
from movie.models import admin as Admin
from movie.models import user as User
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
    movie = data['movie_id']
    user_id = get_user_id(email)

    # check if logged in
    '''if not user_has_login(email, session):
      return {"message": "the user has not logined"}, 400

    # check token
    if not user_is_valid(data):
      return {"message": "Invalid user id"}, 400'''

    # check valid user and movie ids
    if not movie_id_valid(movie):
      return {"message": "Invalid movie id"}, 400

    # check user hasn't already reviewed this movie
    if not user_reviewed_movie(user_id, movie):
      return {"message": "User has not reviewed this movie"}, 400

    review = db.session.query(Review.Reviews).filter(Review.Reviews.user_id == user_id).filter(Review.Reviews.movie_id == movie).first()
    # this shouldn't be possible but check if review exists
    if review == None:
      return {"message": "Review doesn't exist???"}, 400

    db.session.delete(review)
    db.session.commit()

    return {
        "message": "Delete review success"
    }, 200


@review_ns.route('/admin')
class ReviewAdmin(Resource):
  @review_ns.response(200, "Successfully")
  @review_ns.response(400, 'Something went wrong')
  @review_ns.expect(ReviewNS.review_admin_form, validate=True)
  def post(self):
    data = review_ns.payload

    '''
    # check admin has login
    if not user_has_login(data['admin_email'], session):
      return {"message": "the user has not logined"}, 400

    # check admin valid
    data['email'] = data['admin_email']
    if not user_is_valid(data):
      return {"message": "the token is incorrect"}, 400 '''

    # check is admin
    admin = db.session.query(Admin.Admins).filter(Admin.Admins.email == data['admin_email']).first()
    if admin == None:
      return {"message": "Only admin can promote user"}, 400

    # check user valid
    user = db.session.query(User.Users).filter(User.Users.email == data['user_email']).first()
    if user == None:
      return {"message": "The user does not exist"}, 400

    # check user has already be a admin
    if user.is_review_admin == 1:
      return {"message": "The user is already a review admin"}, 400

    # update to admin
    user.is_review_admin = 1
    db.session.commit()
    return {'message': "User is now review admin"}, 200


  @review_ns.response(200, "Delete review success")
  @review_ns.response(400, "Something wrong")
  @review_ns.expect(ReviewNS.review_admin_delete_form, validate=True)
  def delete(self):
    data = review_ns.payload
    email = data['user_email']
    movie = data['movie_id']
    user_id = get_user_id(email)
    admin = data['admin_email']

    # check if logged in
    '''if not user_has_login(admin_email, session):
      return {"message": "the user has not logined"}, 400

    # check token
    if not user_is_valid(data):
      return {"message": "Invalid user id"}, 400'''

    # check valid user and movie ids
    if not movie_id_valid(movie):
      return {"message": "Invalid movie id"}, 400

    # check user hasn't already reviewed this movie
    if not user_reviewed_movie(user_id, movie):
      return {"message": "User has not reviewed this movie"}, 400

    # check if admin is review admin
    deleter = db.session.query(User.Users).filter(User.Users.email == admin).first()
    if deleter.is_review_admin != 1:
      return {"message": 'Not review admin'}, 400

    review = db.session.query(Review.Reviews).filter(Review.Reviews.user_id == user_id).filter(Review.Reviews.movie_id == movie).first()
    # this shouldn't be possible but check if review exists
    if review == None:
      return {"message": "Review doesn't exist???"}, 400

    db.session.delete(review)
    db.session.commit()

    return {
        "message": "Delete review success"
    }, 200

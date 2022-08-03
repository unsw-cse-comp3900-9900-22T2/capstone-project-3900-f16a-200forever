from operator import is_
from attr import validate
from movie.utils.auth_util import check_auth
from sqlalchemy import true
from movie.models import user as User
from movie.models import movie as Movie
from movie import app, request
from flask import session, jsonify
from json import dumps
from flask_restx import Resource, reqparse
from movie import db
from .api_models import UserNS
from movie.utils.other_until import convert_model_to_dict
from movie.utils.user_util import get_user_id


user_ns = UserNS.user_ns

#--------------------GET MOVIE LIST --------------------
@user_ns.route("/movielist")
class MovieList(Resource):
  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, location='args', required=True)
    parser.add_argument('type', type=str, choices=['watched', 'dropped', 'wish'], location='args', required=True)
    args = parser.parse_args()
    email = args['email']
    type = args['type']

    # 1. check the user is valid or not
    user = db.session.query(User.Users).filter(User.Users.email == email).first()
    if user == None:
      return {"message": "the user not exist"},400

    # return
    if type == 'watched':
        result = convert_model_to_dict(user.user_watched_list)
    elif type == "dropped":
        result = convert_model_to_dict(user.user_dropped_list)
    elif type == 'wish':
        result = convert_model_to_dict(user.user_wish_list)
    return {"movies": result}, 200

#--------------------MANAGE WISH LIST--------------------
@user_ns.route('/wishlist')
class WishlistController(Resource):
  @user_ns.response(200, "Successfully")
  @user_ns.response(400, 'Something went wrong')
  @user_ns.expect(UserNS.movie_list_form, validate=True)
  def post(self):
    data = user_ns.payload
    user_id = get_user_id(data['email'])

    # check auth
    message, auth_correct = check_auth(data["email"], data['token'])

    if not auth_correct:
      return {"message", message}, 400

    # check if movie exists
    movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == data['movie_id']).first()
    if movie == None:
      return {'message': 'Movie doesn\'t exist'}, 400

    # check if movie already exists in wishlist
    movie = db.session.query(User.MovieWishList).filter(User.MovieWishList.user_id == user_id, User.MovieWishList.movie_id == data['movie_id']).first()
    if movie != None:
      return {'message': 'Movie already in wishlist'}, 400

    # check if movie is in watched list
    movie = db.session.query(User.MovieWatchedList).filter(User.MovieWatchedList.user_id == user_id, User.MovieWatchedList.movie_id == data['movie_id']).first()
    if movie != None:
      return {'message': 'Movie in watched list cannot be added to wishlist'}, 400

    movie = db.session.query(User.MovieDroppedList).filter(User.MovieDroppedList.user_id == user_id, User.MovieDroppedList.movie_id == data['movie_id']).first()
    if movie != None:
      return {'message': 'Movie in dropped list cannot be added to wishlist'}, 400

    print(data['movie_id'])
    data['user_id'] = user_id
    entry = User.MovieWishList(data)
    db.session.add(entry)
    db.session.commit()

    return {"message:" : "Successfully added movie to wishlist"}, 200


  @user_ns.response(200, "Successfully")
  @user_ns.response(400, 'Something went wrong')
  @user_ns.expect(UserNS.movie_list_form, validate=True)
  def delete(self):
    data = user_ns.payload
    user_id = get_user_id(data['email'])

    # check auth
    message, auth_correct = check_auth(data["email"], data['token'])
    if not auth_correct:
      return {"message", message}, 400

    # check if movie already exists in wishlist
    movie = db.session.query(User.MovieWishList).filter(User.MovieWishList.user_id == user_id, User.MovieWishList.movie_id == data['movie_id']).first()
    if movie == None:
      return {'message': 'Movie not in wishlist'}, 400

    db.session.delete(movie)
    db.session.commit()

    return {"message:" : "Successfully deleted movie from wishlist"}, 200
      
#--------------------MANAGE WATCHED LIST--------------------
@user_ns.route("/watchedlist")
class WatchedMovieList(Resource):
  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  @user_ns.expect(UserNS.movie_list_form, validate=True)
  def post(self):
    data = user_ns.payload
    # check auth
    message, auth_correct = check_auth(data["email"], data['token'])

    if not auth_correct:
      return {"message", message}, 400

    # check the movie id valid
    movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == data['movie_id']).first()
    if movie == None:
      return {"message": "Invalid movie id"}, 400

    # check the movie not in the watchedlist
    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
    print(user.user_watched_list)

    if movie in user.user_watched_list:
      return {"message": "Already in watched list"}, 400

    if movie in user.user_dropped_list:
      user.user_dropped_list.remove(movie)

    if movie in user.user_wish_list:
      user.user_wish_list.remove(movie)

    # check the movie in the dropped list or the wish list
    user.user_watched_list.append(movie)
    db.session.commit()
    return {"message": "Succeffully"}, 200
    
  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  @user_ns.expect(UserNS.movie_list_form, validate=True)
  def delete(self):
    data = user_ns.payload
    # check auth
    message, auth_correct = check_auth(data["email"], data['token'])

    if not auth_correct:
      return {"message", message}, 400


    # check the movie id valid
    movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == data['movie_id']).first()
    if movie == None:
      return {"message": "Invalid movie id"}, 400

    # check the movie not in the watchedlist
    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()

    if movie not in user.user_watched_list:
      return {"message": "Not in watched list"}, 400

    # check the movie in the dropped list or the wish list
    user.user_watched_list.remove(movie)
    db.session.commit()
    return {"message": "Succeffully"}, 200

#--------------------MANAGE DROPPED LIST--------------------
@user_ns.route("/droppedlist")
class DroppedMovieList(Resource):
  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  @user_ns.expect(UserNS.movie_list_form, validate=True)
  def post(self):
    data = user_ns.payload

    # check auth
    message, auth_correct = check_auth(data["email"], data['token'])

    if not auth_correct:
      return {"message", message}, 400

    # check the movie id valid
    movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == data['movie_id']).first()
    if movie == None:
      return {"message": "Invalid movie id"}, 400

    # check the movie not in the droppedlist
    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
    if movie in user.user_dropped_list:
      return {"message": "Movie already in dropped list"}, 400

    if movie in user.user_watched_list:
      user.user_watched_list.remove(movie)

    if movie in user.user_wish_list:
      user.user_wish_list.remove(movie)

    # check the movie in the dropped list or the wish list
    user.user_dropped_list.append(movie)
    db.session.commit()
    return {"message": "Succeffully"}, 200

  @user_ns.response(200, "Successfully")
  @user_ns.response(400, "Something wrong")
  @user_ns.expect(UserNS.movie_list_form, validate=True)
  def delete(self):
    data = user_ns.payload

    # check auth
    message, auth_correct = check_auth(data["email"], data['token'])

    if not auth_correct:
      return {"message", message}, 400

    # check the movie id valid
    movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == data['movie_id']).first()
    if movie == None:
      return {"message": "Invalid movie id"}, 400

    # check the movie not in the droppedlist
    user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
    if movie not in user.user_dropped_list:
      return {"message": "Movie not in dropped list"}, 400

    # check the movie in the dropped list or the wish list
    user.user_dropped_list.remove(movie)
    db.session.commit()
    return {"message": "Succeffully"}, 200
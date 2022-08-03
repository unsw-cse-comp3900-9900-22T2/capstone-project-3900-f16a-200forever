import datetime
from movie.utils.auth_util import check_auth
from movie.models import user as User
from movie.models import movie as Movie
from flask_restx import Resource, reqparse
from movie import db
from .api_models import UserNS
from movie.utils.other_util import convert_model_to_dict
from movie.utils.user_util import get_user_id

movielist = UserNS.user_ns

#--------------------GET MOVIE LIST --------------------
@movielist.route("/movielist")
class MovieList(Resource):
  @movielist.response(200, "Successfully")
  @movielist.response(400, "Something wrong")
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
@movielist.route('/wishlist')
class WishlistController(Resource):
  @movielist.response(200, "Successfully")
  @movielist.response(400, 'Something went wrong')
  @movielist.expect(UserNS.movie_list_form, validate=True)
  def post(self):
    data = movielist.payload
    user_id = get_user_id(data['email'])
    if user_id == None:
      return {"message": "user id not valie"}, 400

    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400

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


  @movielist.response(200, "Successfully")
  @movielist.response(400, 'Something went wrong')
  @movielist.expect(UserNS.movie_list_form, validate=True)
  def delete(self):
    data = movielist.payload
    user_id = get_user_id(data['email'])
    if user_id == None:
      return {"message": "user id not valie"}, 400

    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])
    if not auth_correct:
      return {"message": message}, 400

    # check if movie already exists in wishlist
    movie = db.session.query(User.MovieWishList).filter(User.MovieWishList.user_id == user_id, User.MovieWishList.movie_id == data['movie_id']).first()
    if movie == None:
      return {'message': 'Movie not in wishlist'}, 400

    db.session.delete(movie)
    db.session.commit()

    return {"message:" : "Successfully deleted movie from wishlist"}, 200
      
#--------------------MANAGE WATCHED LIST--------------------
@movielist.route("/watchedlist")
class WatchedMovieList(Resource):
  @movielist.response(200, "Successfully")
  @movielist.response(400, "Something wrong")
  @movielist.expect(UserNS.movie_list_form, validate=True)
  def post(self):
    data = movielist.payload
    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400

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
    data['user_id'] = user.id
    entry = User.MovieWatchedList(data)
    db.session.add(entry)
    db.session.commit()
    return {"message": "Succeffully"}, 200
    
  @movielist.response(200, "Successfully")
  @movielist.response(400, "Something wrong")
  @movielist.expect(UserNS.movie_list_form, validate=True)
  def delete(self):
    data = movielist.payload
    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400


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
@movielist.route("/droppedlist")
class DroppedMovieList(Resource):
  @movielist.response(200, "Successfully")
  @movielist.response(400, "Something wrong")
  @movielist.expect(UserNS.movie_list_form, validate=True)
  def post(self):
    data = movielist.payload

    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400

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

    data['user_id'] = user.id
    entry = User.MovieDroppedList(data)
    db.session.add(entry)
    db.session.commit()
    return {"message": "Succeffully"}, 200

  @movielist.response(200, "Successfully")
  @movielist.response(400, "Something wrong")
  @movielist.expect(UserNS.movie_list_form, validate=True)
  def delete(self):
    data = movielist.payload

    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400

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
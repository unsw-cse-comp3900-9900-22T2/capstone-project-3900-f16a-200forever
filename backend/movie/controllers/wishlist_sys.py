from flask_restx import Resource, reqparse
from flask import session
from movie import db
from movie.controllers.api_models import WishlistNS
from movie.models import user as User
from movie.utils.auth_util import user_has_login, user_is_valid
from movie.utils.user_util import get_user_id
from datetime import datetime

wishlist_ns = WishlistNS.wishlist_ns

@wishlist_ns.route('')
class WishlistController(Resource):
  @wishlist_ns.response(200, "Successfully")
  @wishlist_ns.response(400, 'Something went wrong')
  @wishlist_ns.expect(WishlistNS.edit_list_form, validate=True)
  def post(self):
    data = wishlist_ns.payload
    user_id = get_user_id(data['email'])

    """
    # login
    if not user_has_login(data['email'], session):
      return {"message": "the user has not logined"}, 400

    # valid token
    if not user_is_valid(data):
      return {"message": "the token is incorrect"}, 400
    """

    # check if movie already exists in wishlist
    movie = db.session.query(User.WishlistMovie).filter(User.WishlistMovie.user_id == user_id, User.WishlistMovie.movie_id == data['movie_id']).first()
    if movie != None:
      return {'message': 'Movie already in wishlist'}, 400

    # check if movie is in watched list
    movie = db.session.query(User.WatchedlistMovie).filter(User.WatchedlistMovie.user_id == user_id, User.WatchedlistMovie.movie_id == data['movie_id']).first()
    if movie != None:
      return {'message': 'Movie in watched list cannot be added to wishlist'}, 400

    movie = db.session.query(User.DroppedlistMovie).filter(User.DroppedlistMovie.user_id == user_id, User.DroppedlistMovie.movie_id == data['movie_id']).first()
    if movie != None:
      return {'message': 'Movie in dropped list cannot be added to wishlist'}, 400

    data['user_id'] = user_id
    data['added_time'] = datetime.now()
    entry = User.WishlistMovie(data)
    db.session.add(entry)
    db.session.commit()

    return {"message:" : "Successfully added movie to wishlist"}, 200


  @wishlist_ns.response(200, "Successfully")
  @wishlist_ns.response(400, 'Something went wrong')
  @wishlist_ns.expect(WishlistNS.edit_list_form, validate=True)
  def delete(self):
    data = wishlist_ns.payload
    user_id = get_user_id(data['email'])

    """
    # login
    if not user_has_login(data['email'], session):
      return {"message": "the user has not logined"}, 400

    # valid token
    if not user_is_valid(data):
      return {"message": "the token is incorrect"}, 400
    """

    # check if movie already exists in wishlist
    movie = db.session.query(User.WishlistMovie).filter(User.WishlistMovie.user_id == user_id, User.WishlistMovie.movie_id == data['movie_id']).first()
    if movie == None:
      return {'message': 'Movie not in wishlist'}, 400

    db.session.delete(movie)
    db.session.commit()

    return {"message:" : "Successfully deleted movie from wishlist"}, 200
import imp
from movie.controllers.api_models import RecommendationNS
from movie import db
from movie.models import movie as Movie
from flask_restx import Resource, reqparse
from movie.utils.other_until import convert_model_to_dict
from random import randint
from random import seed

recommendation_ns = RecommendationNS.recommendation_ns
seed(1)

@recommendation_ns.route('/genre')
class RCMGenre(Resource):
  @recommendation_ns.response(200, 'Successfully retrieved genres')
  @recommendation_ns.response(400, 'Something went wrong')
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('movie_id', type=int, location='args', required=True)
    args = parser.parse_args()
    movie_id = args['movie_id']

    # check movie id valid
    movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == movie_id).first()
    if movie == None:
      return {"message": "Invalid movie id"}, 400
    
    # get movie genre
    genres = movie.movie_genre
    ids = [ge.id for ge in genres]
    offset = randint(0, 25799)
    movies = db.session.query(Movie.Movies).filter(Movie.MovieGenre.genre_id.in_(ids)).join(Movie.MovieGenre).order_by(Movie.Movies.total_rating.desc()).limit(100).offset(offset).all()
    return {"movies": convert_model_to_dict(movies)}, 200    
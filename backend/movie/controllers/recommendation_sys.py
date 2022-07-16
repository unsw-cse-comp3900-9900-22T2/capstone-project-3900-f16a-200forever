import imp
from movie.controllers.api_models import RecommendationNS
from movie import db
from movie.models import movie as Movie
from movie.models import person as Person
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

@recommendation_ns.route('/director')
class RCMDirector(Resource):
  @recommendation_ns.response(200, 'Successfully retrieved directors')
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
    
    # get movie director
    directors = db.session.query(Person.MovieDirector).filter(Person.MovieDirector.movie_id == movie_id).all()
    ids = [director.person_id for director in directors]
    offset = randint(0, 25799)
    movie_res = db.session.query(Person.MovieDirector, Movie.Movies).filter(Person.MovieDirector.person_id.in_(ids)).limit(100).offset(offset).all()
    # print(movie_res)
    movies_lst = []
    for movie in movie_res:
      movie_detail = {}
      movie_detail['movie_id'] = movie.Movies.id
      movie_detail['movie_title'] = movie.Movies.title
      movie_detail['tagline'] = movie.Movies.tagline
      movie_detail['backdrop'] = movie.Movies.backdrop
      movie_detail['description'] = movie.Movies.description
      movie_detail['runtime'] = movie.Movies.runtime
      movie_detail['release_time'] = movie.Movies.release_time
      movie_detail['total_rating'] = movie.Movies.total_rating
      movie_detail['rating_count'] = movie.Movies.rating_count

      movies_lst.append(movie_detail)


    return {"movies": movies_lst}, 200
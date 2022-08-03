import imp
from tokenize import String
from movie.controllers.api_models import RecommendationNS
from movie import db
from movie.models import movie as Movie
from movie.models import user as User
from movie.models import review as Review
from flask_restx import Resource, reqparse
from movie.utils.other_until import convert_model_to_dict
from movie.utils.recommendation_util import initialise_movies, top_twenty, calculate_genre, calculate_director, get_genre_director_movie
from random import randint
from random import seed

recommendation_ns = RecommendationNS.recommendation_ns
seed(1)

#----------------RECOMMENDATION------------------
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
    movies_lst = []
    while movies_lst == []:
      offset = randint(0, 25799)
      movie_res = db.session.query(Movie.Movies).filter(Movie.MovieGenre.genre_id.in_(ids)).join(Movie.MovieGenre).order_by(Movie.Movies.total_rating.desc()).limit(100).offset(offset).all()

      for movie in movie_res:
        movie_detail = {}
        movie_detail['movie_id'] = movie.id
        movie_detail['movie_title'] = movie.title
        movie_detail['tagline'] = movie.tagline
        movie_detail['backdrop'] = movie.backdrop
        movie_detail['description'] = movie.description
        movie_detail['runtime'] = movie.runtime
        movie_detail['release_time'] = movie.release_time
        movie_detail['total_rating'] = movie.total_rating
        movie_detail['rating_count'] = movie.rating_count

        movies_lst.append(movie_detail)
    
    return {"movies": movies_lst}, 200  


# TODO only recommended from reviews right now
# Gives 20 recommendations
@recommendation_ns.route('/user')
class RecommendUser(Resource):
  @recommendation_ns.response(200, 'Successfully retrieved genres')
  @recommendation_ns.response(400, 'Something went wrong')
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, location='args', required=True)
    parser.add_argument('by', type=str, location='args', choices=['genre', 'director'])    
    args = parser.parse_args()
    by = None
    if 'by' in args.keys():
      by = args['by']
    user_id = args['user_id']
    # check user id valid
    user = db.session.query(User.Users).filter(User.Users.id == user_id).first()
    if user == None:
      return {"message": "Invalid user id"}, 400
    

    # check if user has reviewed any movies
    reviews = db.session.query(Review.Reviews).filter(Review.Reviews.user_id == user_id).all()
    print(reviews)
    if len(reviews) == 0:
      offset = randint(0, 25799)
      movies = db.session.query(Movie.Movies).limit(20).offset(offset).all()
    else:
      movies = [re.movies for re in reviews]
      genres = []
      directors = []
      for movie in movies:
        tmp = [genre.id for genre in movie.movie_genre]
        genres+=tmp
        tmp = [director.id for director in movie.movie_director_rel]
        directors+=tmp
      # get all movies
      movies = get_genre_director_movie(genres, directors, by)
      print(genres, directors)
      #rec_movies = top_twenty(all_movies)
    return {"movies": convert_model_to_dict(movies)}, 200    
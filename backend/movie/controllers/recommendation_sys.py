import imp
from tokenize import String
from movie.controllers.api_models import RecommendationNS
from movie import db
from movie.models import movie as Movie
from movie.models import user as User
from movie.models import review as Review
from flask_restx import Resource, reqparse
from movie.utils.other_util import convert_model_to_dict
from movie.utils.recommendation_util import get_genre_director_movie
from movie.utils.movie_util import remove_movie_in_the_list
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
    # get arg
    parser = reqparse.RequestParser()
    parser.add_argument('movie_id', type=int, location='args', required=True)
    args = parser.parse_args()
    movie_id = args['movie_id']

    # check movie id valid
    movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == movie_id).first()
    if movie == None:
      return {"message": "Invalid movie id"}, 400
    
    # get movie genre id list
    genres = movie.movie_genre
    ids = [ge.id for ge in genres]
    movies_lst = []

    # get the movies using random
    while movies_lst == []:
      offset = randint(0, 25799)
      movie_res = db.session.query(Movie.Movies).filter(Movie.MovieGenre.genre_id.in_(ids)
      ).join(Movie.MovieGenre).order_by(Movie.Movies.total_rating.desc()).limit(100).offset(offset).all()
      movies_lst = convert_model_to_dict(movie_res)

    return {"movies": movies_lst}, 200  


# Gives 20 recommendations
@recommendation_ns.route('/user')
class RecommendUser(Resource):
  @recommendation_ns.response(200, 'Successfully retrieved genres')
  @recommendation_ns.response(400, 'Something went wrong')
  def get(self):
    # get the argument and body
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
    reviews = db.session.query(Review.Reviews).filter(Review.Reviews.user_id == user_id, Review.Reviews.rating >=3
    ).order_by(Review.Reviews.rating.desc()).all()
    print(reviews)
    # has no review, return 20 movies randomly
    if len(reviews) == 0:
      print(1)
      offset = randint(0, 25799)
      movies = db.session.query(Movie.Movies).limit(20).offset(offset).all()
      return {"movies": convert_model_to_dict(movies)}, 200  
    else:
      # get the top40 movies start from the review with the highest the rating
      # until get 40 movies, and return top 20
      top40_movies = []
      for review in reviews:
        print(review)
        genres = []
        directors = []
        # get the genre id list of the movie
        tmp = [genre.id for genre in review.movies.movie_genre]
        genres+=tmp
        # get the director id list of the movie
        tmp = [director.id for director in review.movies.movie_director_rel]
        directors+=tmp

        # get all movies
        movies = get_genre_director_movie(genres, directors, by)
        top40_movies+=remove_movie_in_the_list(user, movies)
        # only get top 40
        if len(top40_movies) == 40:
          break

      # sort by rating desc
      top40_movies.sort(key=lambda x: x.total_rating)
      top40_movies.reverse()

      return {"movies": convert_model_to_dict(top40_movies)}, 200    



from audioop import reverse
from json import dumps
from movie.utils.movie_until import movie_sort
import movie
from .api_models import MovieNS
from .api_models import GenreNS
from flask_restx import Resource, reqparse
from flask import session
from movie import db
from movie.models import movie as Movie
from movie.models import person as Person
from movie.utils.movie_until import format_movie_return_list
from movie.utils.other_until import convert_object_to_dict, convert_model_to_dict, paging
from operator import attrgetter
from sqlalchemy import and_, null, or_
from movie.models import genre as Genre

genre_ns = GenreNS.genre_ns

@genre_ns.route('/all')
class Genres(Resource):
  @genre_ns.response(200, 'Successfully retrieved genres')
  @genre_ns.response(400, 'Something went wrong')
  def get(self):
    genres_result = db.session.query(Genre.Genres).all()
    genres = {'genres': convert_model_to_dict(genres_result)}

    return genres, 200

@genre_ns.route('/genremovies')
class GenreMovie(Resource):
  @genre_ns.response(200, 'Successfully retrieved movies of this genre')
  @genre_ns.response(400, 'Something went wrong')
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('genre_id', type=int, required=True, location="args")
    parser.add_argument('order', choices=['ascending', 'descending'], type=str, location='args')
    parser.add_argument('num_per_page', type=int, location='args')
    parser.add_argument('page', type=int, location='args')
    args = parser.parse_args()
    genre_id = args['genre_id']

    # defualt the first page is 1
    if args['page'] == None:
      args['page'] = 1

    # default num of movies in one page is 10
    if args['num_per_page'] == None:
      args['num_per_page'] = 10

    # default order by asceding 
    if args['order'] == None:
      args['order'] = 'ascending'
    strategy = args['order']

    genre_movie_result = db.session.query(Genre.Genres, Movie.MovieGenre, Movie.Movies,
    ).with_entities(Movie.Movies.id, Movie.Movies.title, Movie.Movies.backdrop, Movie.Movies.total_rating, Movie.Movies.rating_count,
    ).filter(Genre.Genres.id == genre_id).filter(Movie.Movies.id == Movie.MovieGenre.movie_id,
    ).filter(Genre.Genres.id == Movie.MovieGenre.genre_id).all()
    total_num = len(genre_movie_result)
    movies_lst = []
    for movie in genre_movie_result:
        movie_info = {}
        movie_info['id'] = movie.id
        movie_info['title'] = movie.title
        movie_info['backdrop'] = movie.backdrop
        # if movie.id == 11:
        #     movie_info['total_rating'] = 1000000
        #     movie_info['rating_count'] = 234
        # else:
        movie_info['total_rating'] = movie.total_rating
        movie_info['rating_count'] = movie.rating_count

        movies_lst.append(movie_info)
    
    movies_lst = movie_sort(movies_lst, strategy)

    movies_lst = paging(args['page'], args['num_per_page'], movies_lst)

    movies = {'movies': movies_lst, 'total_num': total_num}
    return movies, 200

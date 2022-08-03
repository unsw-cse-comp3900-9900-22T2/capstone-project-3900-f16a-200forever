from audioop import reverse
from json import dumps
from movie.utils.movie_util import movie_sort
import movie
from .api_models import MovieNS
from flask_restx import Resource, reqparse
from flask import session
from movie import db
from movie.models import movie as Movie
from movie.models import person as Person
from movie.utils.movie_util import format_movie_return_list, adjust_rating
from movie.utils.other_util import convert_object_to_dict, convert_model_to_dict, paging
from movie.utils.user_util import user_id_valid
from operator import attrgetter
from sqlalchemy import and_, null, or_
from movie.models import genre as Genre
 
movie_ns = MovieNS.movie_ns

#--------------------MOVIE SEARCH--------------------
@movie_ns.route("/search")
class SearchMovie(Resource):
  @movie_ns.response(200, "Search successfully")
  @movie_ns.response(400, "Something wrong")
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('type', type=str, location='args')
    parser.add_argument("keywords", type=str, location='args')
    parser.add_argument('order', choices=['ascending', 'descending'], type=str, location='args')
    parser.add_argument('num_per_page', type=int, location='args')
    parser.add_argument('page', type=int, location='args')
    parser.add_argument('user_id', type=str, location="args")
    args = parser.parse_args()

    # defualt the first page is 1
    if args['page'] == None:
      args['page'] = 1

    # default num of movies in one page is 10
    if args['num_per_page'] == None:
      args['num_per_page'] = 12

    if args['order'] == None:
      args['order'] = 'ascending'

    matched_movies = []
    #search by title
    # if args['by_title'] != None and args['by_title'] != '':
    if args['type'] == "movie name":
      # kw = args['by_title']
      kw = args["keywords"]
      result = []
      if args['order'] == 'ascending':
        result = db.session.query(Movie.Movies).filter(Movie.Movies.title.ilike(f'%{kw}%')
        ).order_by(Movie.Movies.total_rating.asc(), Movie.Movies.title
        ).all()
      else:
        result = db.session.query(Movie.Movies).filter(Movie.Movies.title.ilike(f'%{kw}%')
        ).order_by(Movie.Movies.total_rating.desc(), Movie.Movies.title
        ).all()
      matched_movies += result
      
    # search by description 
    # elif args['by_description'] != None and args['by_description'] != '':
    elif args['type'] == 'description':
      # kw = args['by_description']
      kw = args["keywords"]
      result = []
      if args['order'] == 'ascending':
        result = db.session.query(Movie.Movies).filter(Movie.Movies.description.ilike(f'%{kw}%')
        ).order_by(Movie.Movies.total_rating.asc(), Movie.Movies.title
        ).all()
      else:
        result = db.session.query(Movie.Movies).filter(Movie.Movies.description.ilike(f'%{kw}%')
        ).order_by(Movie.Movies.total_rating.desc(), Movie.Movies.title
        ).all()
      matched_movies += result

    # search by director
    # elif args['by_director'] != None and args['by_director'] != '':
    elif args['type'] == 'director':
      # kw = args['by_director']
      kw = args["keywords"]
      result = []
      if args['order'] == 'ascending':
        result = db.session.query(
          Person.MovieDirector, Person.Persons, Movie.Movies, 
        ).filter(
          Person.MovieDirector.movie_id == Movie.Movies.id,
        ).filter(
          Person.MovieDirector.person_id == Person.Persons.id,
        ).filter(
          Person.Persons.name.ilike(f'%{kw}%')
        ).order_by(Movie.Movies.total_rating.asc(), Movie.Movies.title
        ).all()
      else:
        result = db.session.query(
          Person.MovieDirector, Person.Persons, Movie.Movies, 
        ).filter(
          Person.MovieDirector.movie_id == Movie.Movies.id,
        ).filter(
          Person.MovieDirector.person_id == Person.Persons.id,
        ).filter(
          Person.Persons.name.ilike(f'%{kw}%')
        ).order_by(Movie.Movies.total_rating.desc(), Movie.Movies.title
        ).all()
      matched_movies += result
    
    # adjust for banned list
    if args['user_id'] != None:
      # check user id valid
      if not user_id_valid(args['user_id']):
        return {"message": "User id invalid"}, 400
      else:
        for movie in matched_movies:
          movie.total_rating, movie.rating_count = adjust_rating(args['user_id'], movie.id)

    total_num = len(matched_movies)
    # paging
    matched_movies = paging(args['page'], args['num_per_page'], matched_movies)

    movies = []
    if args['type'] != 'director':
      for movie in matched_movies:
        data = convert_object_to_dict(movie)
        year = None
        if movie.release_time != None:
          year = movie.release_time.split('-')[0]
          data['release_time'] = year
          movies.append(data)
      return {"movies": movies, "total": total_num}, 200

    for movie in matched_movies: 
      print(movie)
      year = None
      if movie.Movies.release_time != None:
        year = movie.Movies.release_time.split('-')[0]
      data = convert_object_to_dict(movie.Movies)
      data['release_time'] = year
      print(data)
      movies.append(data)

    return {"movies": movies, "total": total_num}, 200

#-------------------SHOW MOVIE DETAIL-------------------
@movie_ns.route('/moviedetails')
class MovieDetails(Resource):
  @movie_ns.response(200, 'Successfully retrieved movie details')
  @movie_ns.response(400, 'Something went wrong')
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('movie_id', type=int, required=True, location="args")
    parser.add_argument('user_id', type=str, location="args")
    args = parser.parse_args()
    movie_id = args['movie_id']

    select_movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == movie_id).first()
    if select_movie == None:
      return {'message': 'Cannot find movie'}, 400
  
    movie_genre = []
    genre_result = db.session.query(Genre.Genres, Movie.MovieGenre, Movie.Movies).with_entities(Genre.Genres.name).filter(Movie.Movies.id == movie_id).filter(Movie.MovieGenre.movie_id == movie_id).filter(Movie.MovieGenre.genre_id == Genre.Genres.id).all()
    for genre in genre_result:
      genre_name = genre.name
      movie_genre.append(genre_name)

    # title, backdrop, rating
    movie_title = select_movie.title
    movie_backdrop = select_movie.backdrop
    description = select_movie.description
    runtime = select_movie.runtime
    release_time = select_movie.release_time
    release_status = select_movie.release_status

    # adjust for banned list
    if args['user_id'] != None:
      # check user id valid
      if not user_id_valid(args['user_id']):
        return {"message": "User id invalid"}, 400
      else:
        total_rating, rating_count = adjust_rating(args['user_id'], movie_id)
    else:
      rating_count = select_movie.rating_count
      total_rating = select_movie.total_rating

    movie_actors = []
    movie_directors = []
    actor_result = db.session.query(Person.MovieActor, Person.Persons, Movie.Movies).with_entities(Person.Persons.name, Person.MovieActor.character).filter(Person.MovieActor.movie_id == movie_id).filter(Person.Persons.id == Person.MovieActor.person_id).filter(Movie.Movies.id == Person.MovieActor.movie_id).all()
    director_result = db.session.query(Person.MovieDirector, Person.Persons, Movie.Movies).with_entities(Person.Persons.id, Person.Persons.name).filter(Person.MovieDirector.movie_id == movie_id).filter(Person.Persons.id == Person.MovieDirector.person_id).filter(Movie.Movies.id == Person.MovieDirector.movie_id).all()
    for actor in actor_result:
      actor_info = {}
      actor_info['name'] = actor.name
      actor_info['character'] = actor.character
      movie_actors.append(actor_info)
    
    for director in director_result:
      director_info = {}
      director_info['id'] = director.id
      director_info['name'] = director.name
      movie_directors.append(director_info)

    movie_details = {
      'id': movie_id, #str
      'name': movie_title, #str
      'backdrop': movie_backdrop, #str
      'description': description, #str
      'runtime': runtime, #int
      'release_time': release_time, #str
      'release_status': release_status, #str
      'total rating': total_rating, #int
      'rating count': rating_count, #int
      'actors': movie_actors, #list of dict
      'directors': movie_directors, #list of str
      'genres': movie_genre,  #list of str
      'reviews': [] #list of dict
    }
    return movie_details, 200

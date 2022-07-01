from audioop import reverse
from json import dumps
from numpy import require
import movie
from .api_models import MovieNS
from flask_restx import Resource, reqparse
from flask import session
from movie import db
from movie.models import movie as Movie
from movie.models import person as Person
from movie.utils.movie_until import format_movie_return_list
from movie.utils.other_until import convert_object_to_dict, convert_model_to_dict, paging
from operator import attrgetter
from sqlalchemy import and_, or_
 
movie_ns = MovieNS.movie_ns

@movie_ns.route("/search")
class SearchMovie(Resource):
  @movie_ns.response(200, "Search successfully")
  @movie_ns.response(400, "Something wrong")
  def get(self):
    parser = reqparse.RequestParser()
    # parser.add_argument('by_title', type=str, location='args')
    # parser.add_argument('by_description', type=str, location='args')
    # parser.add_argument('by_director', type=str, location='args')
    # parser.add_argument('by_actor', type=str, location='args')
    # parser.add_argument('order', choices=['asc', 'desc'], type=str, location='args')
    # parser.add_argument('page', type=int, location='args')
    # parser.add_argument('num_per_page', type=int, location='args')
    parser.add_argument('type', type=str, location='args')
    parser.add_argument("keywords", type=str, location='args')
    parser.add_argument('order', choices=['ascending', 'descending'], type=str, location='args')
    parser.add_argument('num_per_page', type=int, location='args')
    parser.add_argument('page', type=int, location='args')
    args = parser.parse_args()
    print(args)

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
      if args['order'] == 'descending':
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
      if args['order'] == 'descending':
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
      if args['order'] == 'descending':
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

    # search by actor
    # elif args['by_actor'] != None and args['by_actor'] != '':
    #   kw = args['by_actor']
    #   #result = db.session.query(Movie.Movies).filter(Person.Persons.name.ilike("%{kw}%"))
    #   result = db.session.query(
    #     Person.MovieActor, Person.Persons, Movie.Movies, 
    #   ).filter(
    #     Person.MovieActor.movie_id == Movie.Movies.id,
    #   ).filter(
    #     Person.MovieActor.person_id == Person.Persons.id,
    #   ).filter(
    #     Person.Persons.name.ilike(f'%{kw}%')
    #   ).order_by(Movie.Movies.total_rating.desc(), Movie.Movies.title
    #   ).all()
      
    #   matched_movies += result
     
    # sort 
    #TODO: current sort not consider the banned
    

    total_num = len(matched_movies)
    # paging
    matched_movies = paging(args['page'], args['num_per_page'], matched_movies)

    movies = []
    if args['type'] != 'director':
      for movie in matched_movies:
        data = convert_object_to_dict(movie)
        year = None
        if movie.release_time != None:
          year = movie.release_time.year
          data['release_time'] = year
          movies.append(data)
      return {"movies": movies, "total": total_num}, 200

    for movie in matched_movies: 
      print(movie)
      year = None
      if movie.Movies.release_time != None:
        year = movie.Movies.release_time.year
      data = convert_object_to_dict(movie.Movies)
      data['release_time'] = year
      #data['actors'] = convert_model_to_dict(movie.MovieActor)
      #data['directors'] = convert_model_to_dict(movie.MovieDirector)
      print(data)
      movies.append(data)

    return {"movies": movies, "total": total_num}, 200
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
from operator import attrgetter
 
movie_ns = MovieNS.movie_ns

@movie_ns.route("/search")
class SearchMovie(Resource):
  @movie_ns.response(200, "Search successfully")
  @movie_ns.response(400, "Something wrong")
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('by_title', type=str, location='args')
    parser.add_argument('by_description', type=str, location='args')
    parser.add_argument('by_director', type=str, location='args')
    parser.add_argument('by_actor', type=str, location='args')
    parser.add_argument('order', choices=['asc', 'desc'], type=str, location='args')
    parser.add_argument('page', type=int, location='args')
    args = parser.parse_args()
    print(args)
    matched_movies = []
    #search by title
    if args['by_title'] != None and args['by_title'] != '':
      kw = args['by_title']
      result = db.session.query(Movie.Movies).filter(Movie.Movies.title.ilike(f'%{kw}%')).all()
      matched_movies += result
      
    # search by description 
    if args['by_description'] != None and args['by_description'] != '':
      kw = args['by_description']
      result = db.session.query(Movie.Movies).filter(Movie.Movies.description.ilike(f'%{kw}%')).all()
      matched_movies += result

    # search by director
    if args['by_director'] != None and args['by_director'] != '':
      kw = args['by_director']
      result = db.session.query(
        Person.MovieDirector, Person.Persons, Movie.Movies, 
      ).with_entities(Movie.Movies.id, Movie.Movies.title, Movie.Movies.release_time, Movie.Movies.total_rating).filter(
        Person.MovieDirector.movie_id == Movie.Movies.id,
      ).filter(
        Person.MovieDirector.person_id == Person.Persons.id,
      ).filter(
        Person.Persons.name.ilike(f'%{kw}%')
      ).all()
      matched_movies += result

    # search by actor
    if args['by_actor'] != None and args['by_actor'] != '':
      kw = args['by_actor']
      #result = db.session.query(Movie.Movies).filter(Person.Persons.name.ilike("%{kw}%"))
      result = db.session.query(
        Person.MovieActor, Person.Persons, Movie.Movies, 
      ).with_entities(Movie.Movies.id, Movie.Movies.title, Movie.Movies.release_time, Movie.Movies.total_rating).filter(
        Person.MovieActor.movie_id == Movie.Movies.id,
      ).filter(
        Person.MovieActor.person_id == Person.Persons.id,
      ).filter(
        Person.Persons.name.ilike(f'%{kw}%')
      ).all()
      matched_movies += result
     
    print(matched_movies)
    # sort 
    #TODO: current sort not consider the banned
    if len(matched_movies) != 0 and 'order' == 'asc':
      matched_movies.sort(key=attrgetter('total_rating'))
    elif len(matched_movies) != 0:
      matched_movies.sort(key=attrgetter('total_rating'), reverse=True)

    movies = []
    for movie in matched_movies: 
      data = {}
      data['id'] = movie.id
      data['title'] = movie.title
      if movie.release_time == None:
        data['relese_time'] = "Unknown"
      else:
        data['relese_time'] = movie.release_time.year
      movies.append(data)

    return dumps({"movies": movies}), 200
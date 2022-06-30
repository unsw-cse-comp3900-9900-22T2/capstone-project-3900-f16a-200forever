from audioop import reverse
from email import parser
from json import dumps
from numpy import require
import movie
from .api_models import MovieNS
from flask_restx import Resource, reqparse
from flask import session
from movie import db
from movie.models import movie as Movie
from movie.models import person as Person
from movie.models import genre as Genre
from movie.utils.movie_until import format_movie_return_list
from operator import attrgetter
 
movie_ns = MovieNS.movie_ns

# show the details of the movie
@movie_ns.route('/moviedetails')
class MovieDetails(Resource):
    @movie_ns.response(200, 'Successfully retrieved movie details')
    @movie_ns.response(400, 'Something went wrong')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('movie_id', type=int, required=True)
        args = parser.parse_args()
        movie_id = args['movie_id']

        select_movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == movie_id).first()
        if select_movie == None:
            return dumps({'message': 'Cannot find movie'}), 400
		
        # # genres
        # movie_genre_id = db.session.query(Movie.MovieGenre).filter(Movie.MovieGenre.movie_id == movie_id).all()
        movie_genre = []
        # for genre_id in movie_genre_id:
        #     # genre_id = i['genre_id']
        #     genre = db.session.query(Genre.Genres).filter(Genre.Genres.id == genre_id).first()['name']
        #     movie_genre.append(genre)

        # title, backdrop, rating
        movie_title = select_movie.title
        movie_backdrop = select_movie.backdrop
        rating_count = select_movie.rating_count
        total_rating = select_movie.total_rating
        description = select_movie.description
        runtime = select_movie.runtime
        release_time = str(select_movie.release_time)
        release_status = select_movie.release_status
        '''
        # if the movie has no rating, set it to -1 which will be displayed as no rating
        if rating_count != 0 and total_rating != 0:
            final_rating = total_rating / rating_count
            final_rating = round(final_rating, 1)
        else:
            final_rating = -1
        '''
        # # actors and director
        # movie_actors_id = db.session.query(Person.MovieActor).filter(Person.MovieActor.movie_id == movie_id).all()
        # movie_directors_id = db.session.query(Person.MovieDirector).filter(Person.MovieDirector.movie_id == movie_id).all()
        movie_actors = []
        movie_directors = []
        # # actors [{'actor_name': sample, 'actor_character': sample}, {}...]
        # for i in movie_actors_id:
        #     actor_id = i['person_id']
        #     actor_name = db.session.query(Person.Persons).filter(Person.Persons.id == actor_id).first()['name']
        #     actor_character = i['character']
        #     movie_actors.append({'actor_name': actor_name, 'actor_character': actor_character})

        # # directors [name]
        # for i in movie_directors_id:
        #     director_id = i['person_id']
        #     director_name = db.session.query(Person.Persons).filter(Person.Persons.id == director_id).first()['name']
        #     movie_directors.append(director_name)

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
            'genres': movie_genre,  #list of dict
            'reviews': [] #list of dict
        }
        return dumps(movie_details), 200


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
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

# show the details of the movie
@movie_ns.route('/moviedetails')
class MovieDetails(Resource):
    @movie_ns.response(200, 'Successfully retrieved movie details')
    @movie_ns.response(400, 'Something went wrong')
    def get(self):
        data = movie_ns.payload
        movie_id = data['movie_id']
        select_movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == movie_id).first()
        # genres
        movie_genre_id = db.session.query(Movie.MoviesGenres).filter(Movie.MoviesGenres.movie_id == movie_id).all()
        movie_genre = []
        for i in movie_genre_id:
            genre_id = i['genre_id']
            genre = db.session.query(Movie.Genres).filter(Movie.Genres.id == genre_id).first()['name']
            movie_genre.append(genre)

        if select_movie == None:
            return dumps({'message': 'Cannot find movie'}), 400
        
        # title, backdrop, rating
        movie_title = select_movie['title']
        movie_backdrop = select_movie['backdrop']
        rating_count = select_movie['rating_count']
        total_rating = select_movie['total_rating']
        description = select_movie['description']
        runtime = select_movie['runtime']
        release_time = select_movie['release_time']
        release_status = select_movie['release_status']
        '''
        # if the movie has no rating, set it to -1 which will be displayed as no rating
        if rating_count != 0 and total_rating != 0:
            final_rating = total_rating / rating_count
            final_rating = round(final_rating, 1)
        else:
            final_rating = -1
        '''
        # actors and director
        movie_actors_id = db.session.query(Movie.MovieActor).filter(Movie.MovieActor.movie_id == movie_id).all()
        movie_directors_id = db.session.query(Movie.MovieDirector).filter(Movie.MovieDirector.movie_id == movie_id).all()
        movie_actors = []
        movie_directors = []
        # actors [{'actor_name': sample, 'actor_character': sample}, {}...]
        for i in movie_actors_id:
            actor_id = i['person_id']
            actor_name = db.session.query(Person.Persons).filter(Person.Persons.id == actor_id).first()['name']
            actor_character = i['character']
            movie_actors.append({'actor_name': actor_name, 'actor_character': actor_character})

        # directors [name]
        for i in movie_directors_id:
            director_id = i['person_id']
            director_name = db.session.query(Person.Persons).filter(Person.Persons.id == director_id).first()['name']
            movie_directors.append(director_name)

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
    parser.add_argument('num_per_page', type=int, location='args')
    args = parser.parse_args()
    print(args)

    # defualt the first page is 1
    if args['page'] == None:
      args['page'] = 1

    # default num of movies in one page is 10
    if args['num_per_page'] == None:
      args['num_per_page'] = 10

    matched_movies = []
    #search by title
    if args['by_title'] != None and args['by_title'] != '':
      kw = args['by_title']
      result = db.session.query(Movie.Movies).filter(Movie.Movies.title.ilike(f'%{kw}%')
      ).order_by(Movie.Movies.total_rating.desc(), Movie.Movies.title
      ).all()
      matched_movies += result
      
    # search by description 
    elif args['by_description'] != None and args['by_description'] != '':
      kw = args['by_description']
      result = db.session.query(Movie.Movies).filter(Movie.Movies.description.ilike(f'%{kw}%')
      ).order_by(Movie.Movies.total_rating.desc(), Movie.Movies.title
      ).all()
      matched_movies += result

    # search by director
    elif args['by_director'] != None and args['by_director'] != '':
      kw = args['by_director']
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
    elif args['by_actor'] != None and args['by_actor'] != '':
      kw = args['by_actor']
      #result = db.session.query(Movie.Movies).filter(Person.Persons.name.ilike("%{kw}%"))
      result = db.session.query(
        Person.MovieActor, Person.Persons, Movie.Movies, 
      ).filter(
        Person.MovieActor.movie_id == Movie.Movies.id,
      ).filter(
        Person.MovieActor.person_id == Person.Persons.id,
      ).filter(
        Person.Persons.name.ilike(f'%{kw}%')
      ).order_by(Movie.Movies.total_rating.desc(), Movie.Movies.title
      ).all()
      
      matched_movies += result
     
    # sort 
    #TODO: current sort not consider the banned
    if len(matched_movies) != 0 and args['order'] == 'desc':
      matched_movies.reverse()
      #matched_movies.sort(key=attrgetter('total_rating'), reverse=True)


    total_num = len(matched_movies)
    # paging
    matched_movies = paging(args['page'], args['num_per_page'], matched_movies)

    movies = []
    for movie in matched_movies: 
      print(movie)
      year = None
      if movie.Movies.release_time != None:
        year = movie.Movies.release_time.year
      data = convert_object_to_dict(movie.Movies)
      data['release_time'] = year
      print(movie.MovieActor)
      #data['actors'] = convert_model_to_dict(movie.MovieActor)
      #data['directors'] = convert_model_to_dict(movie.MovieDirector)
      print(data)
      movies.append(data)

    return {"movies": movies, "total": total_num}, 200
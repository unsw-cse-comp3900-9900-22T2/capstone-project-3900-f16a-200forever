from .api_models import MovieNS
from flask_restx import Resource, reqparse
from movie import db
from movie.models import movie as Movie
from movie.models import person as Person
from movie.utils.movie_util import  get_movie_year, get_movie_rating
from movie.utils.other_util import convert_object_to_dict,  paging
from movie.models import genre as Genre
 
movie_ns = MovieNS.movie_ns

#--------------------MOVIE SEARCH--------------------
@movie_ns.route("/search")
class SearchMovie(Resource):
  @movie_ns.response(200, "Search successfully")
  @movie_ns.response(400, "Something wrong")
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('type', choices=['movie name', 'description', 'director', 'actor'], type=str, location='args', required=True)
    parser.add_argument("keywords", type=str, location='args')
    parser.add_argument('order', choices=['ascending', 'descending'], type=str, location='args',default='ascending')
    parser.add_argument('num_per_page', type=int, location='args',default=12)
    parser.add_argument('page', type=int, location='args', default=1)
    parser.add_argument('user_id', type=str, location="args")
    args = parser.parse_args()

    matched_movies = []

    #search by title
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
    elif args['type'] == 'director':
      kw = args["keywords"]
      # get the query that find the movie with the same director
      director_query = db.session.query(
          Person.MovieDirector, Person.Persons, Movie.Movies, 
        ).filter(
          Person.MovieDirector.movie_id == Movie.Movies.id,
        ).filter(
          Person.MovieDirector.person_id == Person.Persons.id,
        ).filter(
          Person.Persons.name.ilike(f'%{kw}%'))

      result = []
      # sort by rating
      if args['order'] == 'ascending':
        result = director_query.order_by(Movie.Movies.total_rating.asc(), Movie.Movies.title).all()
      else:
        result = director_query.order_by(Movie.Movies.total_rating.desc(), Movie.Movies.title).all()
      matched_movies += result

    elif args['type'] == 'actor':
      kw = args["keywords"]
      result = []
      actor_query = db.session.query(
        Person.MovieActor, Person.Persons, Movie.Movies, 
      ).filter(
        Person.MovieActor.movie_id == Movie.Movies.id,
      ).filter(
        Person.MovieActor.person_id == Person.Persons.id,
      ).filter(
        Person.Persons.name.ilike(f'%{kw}%'))

      result = []
      # sort by rating
      if args['order'] == 'ascending':
        result = actor_query.order_by(Movie.Movies.total_rating.asc(), Movie.Movies.title).all()
      else:
        result = actor_query.order_by(Movie.Movies.total_rating.desc(), Movie.Movies.title).all()
      matched_movies += result

    total_num = len(matched_movies)
    # paging
    matched_movies = paging(args['page'], args['num_per_page'], matched_movies)

    movies = []
    for movie in matched_movies:
      if args['type'] == 'director' or args['type'] == 'actor':
        print(movie)
        movie = movie.Movies
      (rating_count, total_rating) = get_movie_rating(args['user_id'], movie)
      movie_detail = convert_object_to_dict(movie)
      movie_detail['total_rating'] = total_rating
      movie_detail['rating_count'] = rating_count
      year = get_movie_year(movie)
      movie_detail['release_time'] = year
      movies.append(movie_detail)
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
    genre_result = db.session.query(Genre.Genres, Movie.MovieGenre, Movie.Movies
    ).with_entities(Genre.Genres.name).filter(Movie.Movies.id == movie_id
    ).filter(Movie.MovieGenre.movie_id == movie_id).filter(Movie.MovieGenre.genre_id == Genre.Genres.id).all()
    for genre in genre_result:
      genre_name = genre.name
      movie_genre.append(genre_name)


    movie_actors = []
    movie_directors = []
    # get given movie actor
    actor_result = db.session.query(Person.MovieActor, Person.Persons, Movie.Movies
    ).with_entities(Person.Persons.name, Person.MovieActor.character
    ).filter(Person.MovieActor.movie_id == movie_id).filter(Person.Persons.id == Person.MovieActor.person_id
    ).filter(Movie.Movies.id == Person.MovieActor.movie_id).all()
    # get given movie director
    director_result = db.session.query(Person.MovieDirector, Person.Persons, Movie.Movies
    ).with_entities(Person.Persons.id, Person.Persons.name).filter(Person.MovieDirector.movie_id == movie_id
    ).filter(Person.Persons.id == Person.MovieDirector.person_id).filter(Movie.Movies.id == Person.MovieDirector.movie_id
    ).all()
    
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

    # adjust for banned list
    (rating_count, total_rating) = get_movie_rating(args['user_id'], select_movie)
    movie_detail = convert_object_to_dict(select_movie)
    movie_detail['total_rating'] = total_rating
    movie_detail['rating_count'] = rating_count
    movie_detail['actors']: movie_actors
    movie_detail['directors']: movie_directors

    return movie_detail, 200

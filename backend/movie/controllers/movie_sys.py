from audioop import reverse
from datetime import datetime
from json import dumps
from numpy import require
from movie.utils.movie_until import movie_sort
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
from sqlalchemy import and_, null, or_
from movie.models import genre as Genre
from movie.models import review as Review
from movie.models import user as User
from sqlalchemy import func
 
movie_ns = MovieNS.movie_ns

@movie_ns.route("/search")
class SearchMovie(Resource):
  @movie_ns.response(200, "Search successfully")
  @movie_ns.response(400, "Something wrong")
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('type', type=str, location='args', required=True)
    parser.add_argument("keywords", type=str, location='args', required=True)
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

# show the details of the movie
@movie_ns.route('/moviedetails')
class MovieDetails(Resource):
  @movie_ns.response(200, 'Successfully retrieved movie details')
  @movie_ns.response(400, 'Something went wrong')
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('movie_id', type=int, required=True, location="args")
    parser.add_argument('review_num_per_page', type=int, location='args')
    parser.add_argument('page', type=int, location='args')
    args = parser.parse_args()
    print(args)
    movie_id = args['movie_id']

    # defualt the first page is 1
    if args['page'] == None:
      args['page'] = 1

    # default num of movies in one page is 5
    if args['review_num_per_page'] == None:
      args['review_num_per_page'] = 5

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
    rating_count = select_movie.rating_count
    total_rating = select_movie.total_rating
    description = select_movie.description
    runtime = select_movie.runtime
    release_time = str(select_movie.release_time)
    release_status = select_movie.release_status

    if rating_count  == None:
        movie_rating = 0
    else:
        movie_rating = round(float(total_rating) / float(rating_count), 1)

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

    # this is a new part for movie reviews
    movie_reviews = [] # this is a list of dictionary
    # reviews_res = db.session.query(Review.Reviews, User.Users, Movie.Movies, Review.ReviewLikes, Review.ReviewUnlikes).with_entities(Review.Reviews.id, Review.Reviews.review_content, Review.Reviews.rating, Review.Reviews.created_time, User.Users.id, User.Users.name, User.Users.image, Review.ReviewLikes.user_id, Review.ReviewUnlikes.user_id).filter(Review.Reviews.movie_id == movie_id).filter(Review.Reviews.user_id == User.Users.id).filter(Movie.Movies.id == Review.Reviews.movie_id).all()
    reviews_res = db.session.query(Review.Reviews, User.Users, func.count(Review.ReviewLikes.review_id), func.count(Review.ReviewUnlikes.review_id)).outerjoin(Review.ReviewLikes, Review.ReviewLikes.review_id == Review.Reviews.id).outerjoin(Review.ReviewUnlikes, Review.ReviewUnlikes.review_id == Review.Reviews.id
      ).filter(Review.Reviews.movie_id == movie_id, Review.Reviews.user_id == User.Users.id
      ).group_by(Review.Reviews.id
      ).all()

    total_num = len(reviews_res)
    reviews_res = paging(args['page'], args['review_num_per_page'], reviews_res)

    for rev in reviews_res:
      review_info = {}
      review = convert_object_to_dict(rev[0])
      user = convert_object_to_dict(rev[1])
      review_info['review_id'] = review['id']
      review_info['review_content'] = review['review_content']
      review_info['rating'] = review['rating']
      review_info['created_time'] = review['created_time']
      review_info['user_id'] = user['id']
      review_info['user_name'] = user['name']
      review_info['user_image'] = user['image']
      review_info['pos_count'] = rev[2]
      review_info['neg_count'] = rev[3]

      movie_reviews.append(review_info)
    

    movie_details = {
      'id': movie_id, #str
      'name': movie_title, #str
      'backdrop': movie_backdrop, #str
      'description': description, #str
      'runtime': runtime, #int
      'release_time': release_time, #str
      'release_status': release_status, #str
      # 'total rating': total_rating, #int
      # 'rating count': rating_count, #int
      'rating': movie_rating, #float
      'actors': movie_actors, #list of dict
      'directors': movie_directors, #list of str
      'genres': movie_genre,  #list of str
      'reviews': movie_reviews #list of dict
    }
    movie_details['review_num'] = total_num
    return movie_details, 200



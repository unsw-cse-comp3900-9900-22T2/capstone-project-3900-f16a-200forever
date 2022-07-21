from movie.models import movie as Movie
from movie.models import review as Review
from movie.models import person as Person

from movie.models import genre as Genre
from movie import db
from sqlalchemy import or_

# put all movies in dictionary with value 0
def initialise_movies():
  all_movies = {}
  movies = db.session.query(Movie.Movies).all()
  for movie in movies:
    all_movies[movie.id] = 0
  return all_movies

# get top 20 movies in dictionary based on value from above
def top_twenty(movies):
  sortlist = sorted(movies.items(), key=lambda x:x[1], reverse=True)
  top = {}
  for i in range(0, 19):
    item = sortlist[i]
    top[item[0]] = item[1]
  top_movies = []
  for movie in top.keys():
    top_movies.append(db.session.query(Movie.Movies).filter(Movie.Movies.id == movie).first())
  return top_movies

# change movie values based on user reviews
# rating 1 = -2, 2 = -1, 3 = 0, 4 = +1, 5 = +2
def calculate_genre( genre_ids):
  movie_genres = db.session.query(Movie.Movies, Movie.MovieGenre).filter(Movie.MovieGenre.movie_id == Movie.Movies.id,  Movie.MovieGenre.genre_id.in_(genre_ids)).all()
  return movie_genres


def calculate_director(directors):
  movie_dir = db.session.query(Person.MovieDirector, Movie.Movies).filter(Person.MovieDirector.movie_id == Movie.Movies.id, Person.MovieDirector.person_id.in_(directors)).all()
  return movie_dir

def get_genre_director_movie(genre_ids, directors):
  movies = db.session.query(Movie.Movies).filter(Movie.MovieGenre.movie_id == Movie.Movies.id, Person.MovieDirector.movie_id == Movie.Movies.id
  ).filter(or_(Movie.MovieGenre.genre_id.in_(genre_ids), Person.MovieDirector.person_id.in_(directors))
  ).order_by(Movie.Movies.total_rating.desc()).limit(20)
  return movies


  """  directors = {}
  for review in reviews:
    movie_directors = db.session.query(Person.MovieDirector).filter(Person.MovieDirector.movie_id == review.movie_id).all()
    for director in movie_directors:
      if director.person_id not in directors:
        directors[director.person_id] = 0
      directors[director.person_id] += review.rating - 3
  
  for director in directors:
    movie_scale = db.session.query(Person.MovieDirector).filter(Person.MovieDirector.person_id == director).all()
    for movie in movie_scale:
      movies[movie.movie_id] += directors[director]
  """

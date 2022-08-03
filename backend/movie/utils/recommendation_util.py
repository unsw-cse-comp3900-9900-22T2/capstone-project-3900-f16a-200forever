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

"""
# change movie values based on user reviews
# rating 1 = -2, 2 = -1, 3 = 0, 4 = +1, 5 = +2
def calculate_genre( genre_ids):
  movie_genres = db.session.query(Movie.Movies, Movie.MovieGenre).filter(Movie.MovieGenre.movie_id == Movie.Movies.id,  Movie.MovieGenre.genre_id.in_(genre_ids)).all()
  return movie_genres

"""

"""
def calculate_director(directors):
  movie_dir = db.session.query(Person.MovieDirector, Movie.Movies).filter(Person.MovieDirector.movie_id == Movie.Movies.id, Person.MovieDirector.person_id.in_(directors)).all()
  return movie_dir
"""


# get the movies which has the same given geenre or give director
# by: the key word that genre or director or both we need to 
# sort by the rating, return the top 20
def get_genre_director_movie(genre_ids, directors, by):
  query = db.session.query(Movie.Movies).filter(Movie.MovieGenre.movie_id == Movie.Movies.id, Person.MovieDirector.movie_id == Movie.Movies.id)

  if by and by == 'genre':
    query = query.filter(Movie.MovieGenre.genre_id.in_(genre_ids))
  if by and by == 'director':
    query = query.filter(Person.MovieDirector.person_id.in_(directors))
  else:
    query = query.filter(or_(Movie.MovieGenre.genre_id.in_(genre_ids), Person.MovieDirector.person_id.in_(directors)))

  # sort
  movies = query.order_by(Movie.Movies.total_rating.desc()).limit(20)
  return movies

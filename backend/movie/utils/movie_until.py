from sqlalchemy import inspect
import movie.models.movie as Movie
from movie import db

def movie_id_valid(id):
  movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == id).first()
  if movie == None:
    return False
  return True

def format_movie_return_list(data):
  movies = []
  for movie in data:
    movie = movie[0]
    data = {}
    data['id'] = movie.id
    data['title'] = movie.title
    if movie.release_time == None:
      data['relese_time'] = "Unknown"
    else:
      data['relese_time'] = movie.release_time.year
    movies.append(data)
  return movies


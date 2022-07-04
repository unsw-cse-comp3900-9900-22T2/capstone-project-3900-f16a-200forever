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

def movie_sort(movies_lst, strategy):
  for movie in movies_lst:
    if movie['rating_count'] == None:
        movie['rating'] = 0
    else:
        movie['rating'] = round(movie['total_rating'] / movie['rating_count'], 1)
  
  if strategy == 'descending':
    movies_lst.sort(key=lambda x:(x.get('rating', 0)), reverse=True)
  elif strategy == 'ascending':
    movies_lst.sort(key=lambda x:(x.get('rating', 0)))
  return movies_lst


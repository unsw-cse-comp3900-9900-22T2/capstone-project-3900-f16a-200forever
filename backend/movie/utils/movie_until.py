import movie.models.movie as Movie
from movie import db

def movie_id_valid(id):
  movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == id).first()
  if movie == None:
    return False
  return True
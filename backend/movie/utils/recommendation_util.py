from movie.models import movie as Movie
from movie.models import review as Review
from movie.models import person as Person
from movie import db

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
def calculate_genre(movies, user):
  reviews = db.session.query(Review.Reviews).filter(Review.Reviews.user_id == user).all()
  genres = {}
  for review in reviews:
    movie_genres = db.session.query(Movie.MovieGenre).filter(Movie.MovieGenre.movie_id == review.movie_id).all()
    for genre in movie_genres:
      if genre.genre_id not in genres:
        genres[genre.genre_id] = 0
      genres[genre.genre_id] += review.rating - 3
  
  for genre in genres:
    movie_scale = db.session.query(Movie.MovieGenre).filter(Movie.MovieGenre.genre_id == genre).all()
    for movie in movie_scale:
      movies[movie.movie_id] += genres[genre]

def calculate_director(movies, user):
  reviews = db.session.query(Review.Reviews).filter(Review.Reviews.user_id == user).all()
  directors = {}
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
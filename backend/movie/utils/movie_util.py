from sqlalchemy import inspect
import movie.models.movie as Movie
import movie.models.user as User
import movie.models.review as Review
from movie.utils.user_util import user_id_valid
from movie import db

# check movie id is valid or not
def movie_id_valid(id):
  movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == id).first()
  if movie == None:
    return False
  return True

# convert movies object into list of dictionary
# change release date to year
def format_movie_return_list(movies):

  result = []
  for movie in movies:
    movie = movie[0]
    data = {}
    data['id'] = movie.id
    data['title'] = movie.title
    if movie.release_time == None:
      data['release_time'] = "Unknown"
    else:
      data['release_time'] = movie.release_time[0:4]
    result.append(data)
  return result 

# sort the movie, sort by rating
def movie_sort(movies_lst, strategy):
  for movie in movies_lst:
    if movie['rating_count'] == None or movie['rating_count'] == 0:
        movie['rating'] = 0
    else:
        movie['rating'] = round(movie['total_rating'] / movie['rating_count'], 1)
  
  if strategy == 'descending':
    movies_lst.sort(key=lambda x:(x.get('rating', 0)), reverse=True)
  elif strategy == 'ascending':
    movies_lst.sort(key=lambda x:(x.get('rating', 0)))
  return movies_lst

# caculate the rating based on the given user banned list
def adjust_rating(user_id, movie_id):
  banned_list = db.session.query(User.BannedList).filter(User.BannedList.user_id == user_id).all()
  movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == movie_id).first()
  total_rating = movie.total_rating
  rating_count = movie.rating_count
  for banned in banned_list:
    review = db.session.query(Review.Reviews).filter(Review.Reviews.user_id == banned.banned_user_id, Review.Reviews.movie_id == movie_id).first()
    if review != None:
      total_rating -= review.rating * review.weight
      rating_count -= review.weight
  return total_rating, rating_count


# get the year of the movie
def get_movie_year(movie):
    year = None
    if movie.release_time != None:
      year = movie.release_time.split('-')[0]
    return year

def get_movie_rating(user_id, select_movie):
  # adjust for banned list
  if user_id != None:
    # check user id valid
    if not user_id_valid(user_id):
      return {"message": "User id invalid"}, 400
    else:
      total_rating, rating_count = adjust_rating(user_id, select_movie.id)
  else:
    rating_count = select_movie.rating_count
    total_rating = select_movie.total_rating
  return (rating_count, total_rating)

# remove the movie in the given movie list that in user's droplist, watchlist, wishlit
def remove_movie_in_the_list(user, movies):
  result = []
  for movie in movies:
    if movie not in user.user_wish_list and movie not in  user.user_dropped_list \
    and movie not in user.user_watched_list:
      result.append(movie)

  return result
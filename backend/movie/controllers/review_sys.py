from pyrsistent import b
from movie.controllers.api_models import ReviewNS
from movie import db
from flask_restx import Resource, reqparse
from movie.models import movie as Movie
from movie.models import review as Review
from sqlalchemy import func
from movie.utils.other_until import paging

review_ns = ReviewNS.review_ns

@review_ns.route('/sort')
class ReviewSort(Resource):
  @review_ns.response(200, 'Successfully')
  @review_ns.response(400, 'Something went wrong')
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('type', type=str, location='args', required=True)
    parser.add_argument('num_per_page', type=int, location='args')
    parser.add_argument('page', type=int, location='args')
    parser.add_argument('movie_id', type=int, location='args', required=True)
    args = parser.parse_args()

    movie_id = args['movie_id']
    
    # defualt the first page is 1
    if args['page'] == None:
      args['page'] = 1

    # default num of movies in one page is 10
    if args['num_per_page'] == None:
      args['num_per_page'] = 12

    # check movie
    movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == movie_id).first()
    if movie == None:
      return {"message": "Invalid movie id"}, 400

    reviews = None
    # sort by the create time
    if args['type'] == 'time':
      reviews = db.session.query(Review.Reviews).filter(Review.Reviews.movie_id == movie_id
      ).order_by(Review.Reviews.created_time.asc(), Review.Reviews.id
      ).all()

    # sort by the likes
    if args['type'] == 'likes':
      reviews = db.session.query(Review.Reviews).filter(Review.Reviews.movie_id == movie_id).join(Review.ReviewLikes
      ).group_by(Review.Reviews.id).order_by(func.count(Review.ReviewLikes.review_id).desc()).all()

    # sort by unlikes
    if args['type'] == 'unlikes':
      reviews = db.session.query(Review.Reviews).filter(Review.Reviews.movie_id == movie_id).join(Review.ReviewUnlikes
      ).group_by(Review.Reviews.id).order_by(func.count(Review.ReviewUnlikes.review_id).desc()).all()

    if reviews == None:
      return {"Something wrong"}, 400

    # paging
    total_num = len(reviews)
    # paging
    matched_movies = paging(args['page'], args['num_per_page'], reviews)
    return {"total": total_num, "reviews": reviews}



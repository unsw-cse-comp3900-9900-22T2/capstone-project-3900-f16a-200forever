from movie.controllers.api_models import ReviewNS
from movie import db
from flask_restx import Resource, reqparse
from movie.models import movie as Movie
from movie.models import review as Review
from movie.models import user as User
from sqlalchemy import func
from movie.utils.other_until import paging, convert_object_to_dict

review_ns = ReviewNS.review_ns

@review_ns.route('/sort')
class ReviewSort(Resource):
  @review_ns.response(200, 'Successfully')
  @review_ns.response(400, 'Something went wrong')
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('type', choices=['time', 'likes', 'unlikes'], type=str, location='args', required=True)
    parser.add_argument('order', choices=['ascending', 'descending'], type=str, location='args', required=True)
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

    # sort by the create time

    if args['type'] == 'time':
      query =  db.session.query(Review.Reviews, User.Users, func.count(Review.ReviewLikes.review_id), func.count(Review.ReviewUnlikes.review_id)).outerjoin(Review.ReviewLikes, Review.ReviewLikes.review_id == Review.Reviews.id).outerjoin(Review.ReviewUnlikes, Review.ReviewUnlikes.review_id == Review.Reviews.id
      ).filter(Review.Reviews.movie_id == movie_id, Review.Reviews.user_id == User.Users.id
      ).group_by(Review.Reviews.id
      )
      if args['order'] == 'ascending':
        all_reviews = query.order_by(Review.Reviews.created_time.desc(), Review.Reviews.id).all()
      else:
        all_reviews = query.order_by(Review.Reviews.created_time.asc(), Review.Reviews.id).all()

    # sort by the likes
    if args['type'] == 'likes':
      all_reviews = db.session.query(Review.Reviews, User.Users, func.count(Review.ReviewLikes.review_id), func.count(Review.ReviewUnlikes.review_id)).outerjoin(Review.ReviewLikes, Review.ReviewLikes.review_id == Review.Reviews.id).outerjoin(Review.ReviewUnlikes, Review.ReviewUnlikes.review_id == Review.Reviews.id
      ).filter(Review.Reviews.movie_id == movie_id, Review.Reviews.user_id == User.Users.id
      ).group_by(Review.Reviews.id
      )
      if args['order'] == 'ascending':
        all_reviews = query.order_by(func.count(Review.ReviewLikes.review_id).desc(), Review.Reviews.created_time.desc()
      ).all()
      else:
        all_reviews = query.order_by(func.count(Review.ReviewLikes.review_id).asc(), Review.Reviews.created_time.desc()
      ).all()


    # sort by unlikes
    if args['type'] == 'unlikes':
      all_reviews = db.session.query(Review.Reviews, User.Users, func.count(Review.ReviewLikes.review_id), func.count(Review.ReviewUnlikes.review_id)).outerjoin(Review.ReviewLikes, Review.ReviewLikes.review_id == Review.Reviews.id).outerjoin(Review.ReviewUnlikes, Review.ReviewUnlikes.review_id == Review.Reviews.id
      ).filter(Review.Reviews.movie_id == movie_id, Review.Reviews.user_id == User.Users.id
      ).group_by(Review.Reviews.id
      )
      if args['order'] == 'ascending':
        all_reviews = query.order_by(func.count(Review.ReviewUnlikes.review_id).desc(), Review.Reviews.created_time.desc()
      ).all()
      else:
        all_reviews = query.order_by(func.count(Review.ReviewUnlikes.review_id).asc(), Review.Reviews.created_time.desc()
      ).all()

    if all_reviews == None:
      return {"Something wrong"}, 400
    
    # paging
    total_num = len(all_reviews)
    # paging
    matched_movies = paging(args['page'], args['num_per_page'], all_reviews)
    result = []
    for mo in matched_movies:
      review = convert_object_to_dict(mo[0])
      user = convert_object_to_dict(mo[1])
      review['likes_count'] = mo[2]
      review['unlikes_count'] = mo[3]
      review['user_email'] = user['email']
      review['user_name'] = user['name']
      review['user_image'] = user['image']
      result.append(review)
      

    return {"total": total_num, "reviews": result}





review_ns = ReviewNs.review_ns

@review_ns.route('/react')
class ReactToReview(Resource):
    @review_ns.response(200, "Add reaction successfully")
    @review_ns.response(400, "Something wrong")
    @review_ns.expect(ReviewNs.validation_check, validate=True)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('review_id', type=str, location='args', required=True)
        parser.add_argument('reaction',choices=['like', 'unlike'], type=str, location='args', required=True)
        args = parser.parse_args()
        review_id = args['review_id']
        reaction = args['reaction']

        data = review_ns.payload
        """
        if not user_has_login(data['email'], session):
          return {"message": "the user has not logined"}, 400

        # check the user is valid or not
        if not user_is_valid(data):
          return {"message": "the token is incorrect"}, 400"""


        user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
        if user == None:
          return {"message": "User not exist"}, 400

        data = {'review_id': review_id, 'user_id': user.id}

        like = db.session.query(Review.ReviewLikes).filter(Review.ReviewLikes.review_id == review_id, Review.ReviewLikes.user_id == user.id).first()
        unlike = db.session.query(Review.ReviewUnlikes).filter(Review.ReviewUnlikes.review_id == review_id, Review.ReviewUnlikes.user_id == user.id).first()
        # positive reaction
        if reaction == "like":
          # delete the like
          if like is not None:
            db.session.delete(like)
            db.session.commit()
          # like failed
          elif like is None and unlike is not None:
            return {"message": "You have unliked this review"}, 400
          # like
          elif like is None and unlike is None:
            react = Review.ReviewLikes(data)
            db.session.add(react)
            db.session.commit()
        # negative reaction
        elif reaction == "unlike":
          # delete the unlike
          if unlike is not None:
            db.session.delete(unlike)
            db.session.commit()
          # unlike failed
          elif unlike is None and like is not None:
            return {"message": "You have liked this review"}, 400
          # unlike
          elif unlike is None and like is None:
            reaction = Review.ReviewUnlikes(data)
            db.session.add(reaction)
            db.session.commit()

        return {"message": "Successfully"}, 200

from .api_models import ReviewNS
from movie import db
from flask_restx import Resource, reqparse
from movie.models import movie as Movie
from movie.models import review as Review
from movie.models import user as User
from sqlalchemy import func
from movie.utils.other_until import paging, convert_object_to_dict
from movie.utils.movie_until import movie_id_valid
from movie.utils.auth_util import user_is_valid, user_has_login
from movie.utils.review_util import user_reviewed_movie, calculate_weight
from movie.utils.user_util import get_user_id
from movie.models import admin as Admin
import uuid
from datetime import datetime

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



@review_ns.route('/react')
class ReactToReview(Resource):
    @review_ns.response(200, "Add reaction successfully")
    @review_ns.response(400, "Something wrong")
    @review_ns.expect(ReviewNS.validation_check, validate=True)
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


review_ns = ReviewNS.review_ns

# user profile page
@review_ns.route('')
class ReviewController(Resource):
  @review_ns.response(200, "Create review success")
  @review_ns.response(400, "Something wrong")
  @review_ns.expect(ReviewNS.review_create_form, validate=True)
  def post(self):
    data = review_ns.payload
    email = data['email']
    movie = data['movie_id']
    rating = data['rating']
    user_id = get_user_id(email)


    # check if logged in
    '''if not user_has_login(email, session):
      return {"message": "the user has not logined"}, 400

    # check token
    if not user_is_valid(data):
      return {"message": "Invalid user id"}, 400'''

    # check rating between 1-5
    if rating < 1 or rating > 5:
      return {"message": "Rating should be 1-5"}, 400

    # check valid user and movie ids
    if not movie_id_valid(movie):
      return {"message": "Invalid movie id"}, 400

    # check user hasn't already reviewed this movie
    if user_reviewed_movie(user_id, movie):
      return {"message": "User already reviewed this movie"}, 400

    data['id'] = str(uuid.uuid4())
    data['user_id'] = user_id
    data['created_time'] = datetime.now()
    data['weight'] = calculate_weight(user_id, movie)

    # commit into db
    new_review = Review.Reviews(data)
    this_movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == movie).first()
    this_movie.total_rating += rating * data['weight']
    if this_movie.rating_count == None:
      this_movie.rating_count = 0
    this_movie.rating_count += data['weight']
    print(new_review)
    db.session.add(new_review)
    db.session.commit()

    return {
        "message": "Create review success"
    }, 200


  @review_ns.response(200, "Delete review success")
  @review_ns.response(400, "Something wrong")
  @review_ns.expect(ReviewNS.review_delete_form, validate=True)
  def delete(self):
    data = review_ns.payload
    email = data['email']
    review_id = data['review_id']
    #user_id = get_user_id(email)

    # check if logged in
    '''if not user_has_login(email, session):
      return {"message": "the user has not logined"}, 400

    # check token
    if not user_is_valid(data):
      return {"message": "Invalid user id"}, 400'''

    # check review valid
    review = db.session.query(Review.Reviews).filter(Review.Reviews.id == review_id).first()
    if review == None:
      return {"message": "Invalid review id"}, 400

    # check permission
    if review.user.email != email:
      user = db.session.query(User.Users).filter(User.Users.email == email).first()
      if user is not None and user.is_review_admin != 1:
        print(user.is_review_admin)
        return {'message': 'No permission'}, 400
      # check admin
      if user is None:
        admin = db.session.query(Admin.Admins).filter(Admin.Admins.email == email).first()
        if admin == None:
          return {'message': 'No permission'}, 400
    
    # delete 
    movie_id = review.movie_id
    this_movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == movie_id).first()
    this_movie.rating_count -= review.weight
    this_movie.total_rating -= review.rating
    db.session.delete(review)
    db.session.commit()

    return {
        "message": "Delete review success"
    }, 200 


@review_ns.route('/admin')
class ReviewAdmin(Resource):
  @review_ns.response(200, "Successfully")
  @review_ns.response(400, 'Something went wrong')
  @review_ns.expect(ReviewNS.review_admin_form, validate=True)
  def post(self):
    data = review_ns.payload

    '''
    # check admin has login
    if not user_has_login(data['admin_email'], session):
      return {"message": "the user has not logined"}, 400

    # check admin valid
    data['email'] = data['admin_email']
    if not user_is_valid(data):
      return {"message": "the token is incorrect"}, 400 '''

    # check is admin
    admin = db.session.query(Admin.Admins).filter(Admin.Admins.email == data['admin_email']).first()
    if admin == None:
      return {"message": "Only admin can promote user"}, 400

    # check user valid
    user = db.session.query(User.Users).filter(User.Users.email == data['user_email']).first()
    if user == None:
      return {"message": "The user does not exist"}, 400

    # check user has already be a admin
    if user.is_review_admin == 1:
      return {"message": "The user is already a review admin"}, 400

    # update to admin
    user.is_review_admin = 1
    db.session.commit()
    return {'message': "User is now review admin"}, 200

"""
  @review_ns.response(200, "Delete review success")
  @review_ns.response(400, "Something wrong")
  @review_ns.expect(ReviewNS.review_admin_delete_form, validate=True)
  def delete(self):
    data = review_ns.payload
    email = data['user_email']
    movie = data['movie_id']
    user_id = get_user_id(email)
    admin = data['admin_email']

    # check if logged in
    '''if not user_has_login(admin_email, session):
      return {"message": "the user has not logined"}, 400

    # check token
    if not user_is_valid(data):
      return {"message": "Invalid user id"}, 400'''

    # check valid user and movie ids
    if not movie_id_valid(movie):
      return {"message": "Invalid movie id"}, 400

    # check user hasn't already reviewed this movie
    if not user_reviewed_movie(user_id, movie):
      return {"message": "User has not reviewed this movie"}, 400

    # check if admin is review admin
    deleter = db.session.query(User.Users).filter(User.Users.email == admin).first()
    if deleter.is_review_admin != 1:
      return {"message": 'Not review admin'}, 400

    review = db.session.query(Review.Reviews).filter(Review.Reviews.user_id == user_id).filter(Review.Reviews.movie_id == movie).first()
    # this shouldn't be possible but check if review exists
    if review == None:
      return {"message": "Review doesn't exist???"}, 400

    this_movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == movie).first()

    this_movie.rating_count -= review.weight
    this_movie.total_rating -= review.rating

    db.session.delete(review)
    db.session.commit()

    return {
        "message": "Delete review success"
    }, 200
"""

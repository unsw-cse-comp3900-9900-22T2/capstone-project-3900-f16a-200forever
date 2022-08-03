from .api_models import ReviewNS
from movie import db
from flask_restx import Resource, reqparse
from movie.models import movie as Movie
from movie.models import review as Review
from movie.models import user as User
from sqlalchemy import func
from movie.utils.other_util import convert_object_to_dict
from movie.utils.movie_util import movie_id_valid
from movie.utils.auth_util import check_auth
from movie.utils.review_util import user_reviewed_movie, calculate_weight, adjust_reviews
from movie.utils.user_util import get_user_id, user_id_valid
from movie.models import admin as Admin
import uuid
from datetime import datetime 

review_ns = ReviewNS.review_ns

#--------------------GET REVIEW LIST--------------------
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
    parser.add_argument('user_id', type=str, location="args")
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


    query_like =  db.session.query(Review.Reviews, User.Users, func.count(Review.ReviewLikes.user_id)
    ).outerjoin(Review.ReviewLikes, Review.ReviewLikes.review_id == Review.Reviews.id
    ).filter(Review.Reviews.movie_id == movie_id, Review.Reviews.user_id == User.Users.id
    ).group_by(Review.Reviews.id)

    query_unlike = db.session.query(Review.Reviews, User.Users, func.count(Review.ReviewUnlikes.user_id)
    ).outerjoin(Review.ReviewUnlikes, Review.ReviewUnlikes.review_id == Review.Reviews.id
    ).filter(Review.Reviews.movie_id == movie_id, Review.Reviews.user_id == User.Users.id
    ).group_by(Review.Reviews.id)


    all_reviews = None
    left = None
    # sort by the create time
    if args['type'] == 'time':
      if args['order'] == 'descending':
        all_reviews = query_like.order_by(Review.Reviews.created_time.desc(), Review.Reviews.id).all()
      else:
        all_reviews = query_like.order_by(Review.Reviews.created_time.asc(), Review.Reviews.id).all()
      left = query_unlike.all()



    # sort by the likes
    if args['type'] == 'likes':
      if args['order'] == 'descending':
        all_reviews = query_like.order_by(func.count(Review.ReviewLikes.review_id).desc(), Review.Reviews.created_time.desc()
      ).all()
      else:
        all_reviews = query_like.order_by(func.count(Review.ReviewLikes.review_id).asc(), Review.Reviews.created_time.desc()
      ).all()
      left = query_unlike.all()


    # sort by unlikes
    if args['type'] == 'unlikes':
      if args['order'] == 'descending':
        all_reviews = query_unlike.order_by(func.count(Review.ReviewUnlikes.review_id).desc(), Review.Reviews.created_time.desc()
      ).all()
      else:
        all_reviews = query_unlike.order_by(func.count(Review.ReviewUnlikes.review_id).asc(), Review.Reviews.created_time.desc()
      ).all()
      left = query_like.all()

    if all_reviews == None and left == None:
      return {"Something wrong"}, 400

    # format left data
    left_data = {}
    for re in left:
      review = convert_object_to_dict(re[0])
      left_data[review['id']] = re[2]

    # adjust for banned list
    if args['user_id'] != None:
      # check user id valid
      if not user_id_valid(args['user_id']):
        return {"message": "User id invalid"}, 400
      else:
        all_reviews = adjust_reviews(args['user_id'], all_reviews)

    # format:
    total_num = len(all_reviews)
    result = []
    print(all_reviews)

    for review in all_reviews:
      data = convert_object_to_dict(review[0])
      user = review[1]
      if args['type'] == 'unlikes':
        data['likes_count'] = left_data[review[0].id]
        data['unlikes_count'] = review[2]
      elif args['type'] != 'unlikes':
        data['unlikes_count'] = left_data[review[0].id]
        data['likes_count'] = review[2]
      data['user_email'] = user.email
      data['user_name'] = user.name
      image = None
      profile_picture = user.image
      if profile_picture is not None:
        image = str(profile_picture.decode())
      data['user_image'] = image
      result.append(data)

    return {"total": total_num, "reviews": result}

#---------------REACT TO REVIEW---------------
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

 
        # check auth
        message, auth_correct = check_auth(data['email'], data['token'])

        if not auth_correct:
          return {"message": message}, 400


        user = db.session.query(User.Users).filter(User.Users.email == data['email']).first()
        if user == None:
          return {"message": "User not exist"}, 400

        data = {'review_id': review_id, 'user_id': user.id}
        is_remove = -1
        like = db.session.query(Review.ReviewLikes
        ).filter(Review.ReviewLikes.review_id == review_id, Review.ReviewLikes.user_id == user.id).first()
        unlike = db.session.query(Review.ReviewUnlikes
        ).filter(Review.ReviewUnlikes.review_id == review_id, Review.ReviewUnlikes.user_id == user.id).first()
        # positive reaction
        if reaction == "like":
          # delete the like
          if like is not None:
            db.session.delete(like)
            is_remove = 0
            db.session.commit()
          # like failed
          elif like is None and unlike is not None:
            return {"message": "You have unliked this review"}, 400
          # like
          elif like is None and unlike is None:
            react = Review.ReviewLikes(data)
            db.session.add(react)
            is_remove = 1
            db.session.commit()
        # negative reaction
        elif reaction == "unlike":
          # delete the unlike
          if unlike is not None:
            db.session.delete(unlike)
            is_remove = 0
            db.session.commit()
          # unlike failed
          elif unlike is None and like is not None:
            return {"message": "You have liked this review"}, 400
          # unlike
          elif unlike is None and like is None:
            reaction = Review.ReviewUnlikes(data)
            db.session.add(reaction)
            is_remove = 1 
            db.session.commit()

        return {"is_remove": is_remove}, 200


review_ns = ReviewNS.review_ns

#---------------MANAGE REVIEW---------------
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
    if user_id == None:
      return {"message": "user id not valie"}, 400

 
    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400

    # check rating between 0-5
    if rating < 0 or rating > 5:
      return {"message": "Rating should be 0-5"}, 400

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
    print(new_review.weight)
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
 
    # check auth
    message, auth_correct = check_auth(data['email'], data['token'])

    if not auth_correct:
      return {"message": message}, 400

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

    # delete likes and unlikes for this review
    #likes = db.session.query(Review.ReviewLikes).filter(Review.ReviewLikes.review_id == review.id).all()
    #db.session.delete(likes)
    #unlikes = db.session.query(Review.ReviewUnlikes).filter(Review.ReviewUnlikes.review_id == review.id).all()
    #db.session.delete(unlikes)
    db.session.commit()

    return {
        "message": "Delete review success"
    }, 200 

#---------------MANAGE REVIEW ADMIN---------------
@review_ns.route('/admin')
class ReviewAdmin(Resource):
  @review_ns.response(200, "Successfully")
  @review_ns.response(400, 'Something went wrong')
  @review_ns.expect(ReviewNS.review_admin_form, validate=True)
  def put(self):
    data = review_ns.payload

    # check auth
    message, auth_correct = check_auth(data["admin_email"], data['token'])

    #if not auth_correct:
    #  return {"message": message}, 400

    # check is admin
    admin = db.session.query(Admin.Admins).filter(Admin.Admins.email == data['admin_email']).first()
    if admin == None:
      return {"message": "Only admin can promote user"}, 400

    # check user valid
    user = db.session.query(User.Users).filter(User.Users.email == data['user_email']).first()
    if user == None:
      return {"message": "The user does not exist"}, 400

    # promoting
    if data['become_admin'] == True:
      # check if user is already a review admin
      if user.is_review_admin == 1:
        return {"message": "The user is already a review admin"}, 400
      else:
        # update to admin
        user.is_review_admin = 1
    # demoting
    else:
      # check if user is already a review admin
      if user.is_review_admin == 0:
        return {"message": "The user is not a review admin"}, 400
      else:
        # demote from admin
        user.is_review_admin = 0

    db.session.commit()
    return {'message': "User is now review admin"}, 200

from tkinter import E
from attr import validate
from movie import db
from .api_models import ReviewNs
from flask_restx import Resource, Api
from movie.models import user as User
from movie.models import review as Review
from flask_restx import Resource, reqparse


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
from movie.models import review as Review
from flask_restx import Resource, reqparse
from .api_models import ReviewNS
from json import dumps
from flask import session, jsonify
from movie import db
import datetime


review_ns = ReviewNS.review_ns

# user profile page
@review_ns.route('/review')
class ReviewController(Resource):
  @review_ns.response(200, "Add review success")
  @review_ns.response(400, "Something wrong")
  @review_ns.expect(ReviewNS.review_create_form, validate=True)
  def post(self):
    data = review_ns.payload
    user = data['user_id']
    movie = data['movie_id']
    rating = data['rating']
    content = data['review_content']

    id = db.session.query(Review.Reviews).count() + 1
    #data['id'] = review.id + 1
    data['id'] = id
    data['created_time'] = datetime.datetime.now()
    data['weight'] = 1

    # commit into db
    new_review = Review.Reviews(data)
    print(new_review)
    db.session.add(new_review)
    db.session.commit()

    return {
        "Review success"
    }, 200
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
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('review_id', type=str, location='args', required=True)
        parser.add_argument('reaction', type=str, location='args', required=True)
        parser.add_argument('user_id', type=str, location='args', required=True)
        args = parser.parse_args()
        review_id = args['review_id']
        reaction = args['reaction']
        user_id = args['user_id']
        # data = review_ns.payload
        # review_id = data['review_id']
        # reaction = data['reaction']
        # user_id = data['user_id']
        data = {'review_id': review_id, 'user_id': user_id}
        # positive reaction
        if reaction == "positive":
            new_positive_reaction = Review.ReviewLikes(data)
            db.session.add(new_positive_reaction)
            db.session.commit()
        # negative reaction
        elif reaction == "negative":
            new_negative_reaction = Review.ReviewUnlikes(data)
            db.session.add(new_negative_reaction)
            db.session.commit()

        return {"message": "Reaction added successfully"}, 200
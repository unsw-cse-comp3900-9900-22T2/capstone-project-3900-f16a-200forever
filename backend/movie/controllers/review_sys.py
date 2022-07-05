from movie import db
from .api_models import ReviewNs
from flask_restx import Resource, Api
from movie.models import user as User
from movie.models import review as Review

review_ns = ReviewNs.review_ns

@review_ns.route('/react')
class ReactToReview(Resource):
    @review_ns.response(200, "Add reaction successfully")
    @review_ns.response(400, "Something wrong")
    def post(self):
        data = review_ns.payload
        review_id = data['review_id']
        reaction = data['reaction']
        user_id = data['user_id']

        # positive reaction
        if reaction == "positive":
            new_positive_reaction = Review.ReviewLikes(review_id=review_id, user_id=user_id)
            db.session.add(new_positive_reaction)
            db.session.commit()
        # negative reaction
        elif reaction == "negative":
            new_negative_reaction = Review.ReviewUnlikes(review_id=review_id, user_id=user_id)
            db.session.add(new_negative_reaction)
            db.session.commit()

        return {"message": "Reaction added successfully"}, 200
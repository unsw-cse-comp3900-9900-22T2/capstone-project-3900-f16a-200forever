from movie import db
from sqlalchemy import *

class Reviews(db.Model):
    __tablename__ = 't_reviews'
    id = db.Column('id', db.Integer, primary_key=True)
    movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('t_movies.id'))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('t_users.id'))
    review_content = db.Column('review_content', db.String(256), nullable=False)
    create_time = db.Column('create_time', db.DateTime, nullable=False)
    rating = db.Column('rating', db.Integer, nullable=False)
    weight = db.Column('weight', db.Float(20), nullable=False)
    # relationships
    # review_likes = db.ralationship('ReviewLikes', back_populates='reviews', lazy=True)
    # review_unlikes = db.relationship('ReviewUnlikes', back_populates='reviews', lazy=True)
    # review_likes_rel = db.relationship(
    #     "ReviewLikes",
    #     back_populates="reviews",
    #     lazy=True,
    #     overlaps="review_unlikes_rel"
    # )
    # review_unlikes_rel = db.relationship(
    #     "ReviewUnlikes",
    #     back_populates="reviews",
    #     lazy=True,
    #     overlaps="review_likes_rel"
    # )

    # def __repr__(self):
    #     return '<Review id:{}>'.format(self.id)  

    # def __init__(self, data):
    #     self.id = data['id']
#         self.movie_id = data['movie_id']
#         self.user_id = data['user_id']
#         self.review_content = data['review_content']
#         self.create_time = data['create_time']
#         self.rating = data['rating']
#         self.weight = data['weight']

# class ReviewLikes(db.Model):
#     __tablename__ = 'r_review_likes'
#     review_id = db.Column('review_id', db.Integer, db.ForeignKey('t_reviews.id'))
#     user_id = db.Column('user_id', db.Integer, db.ForeignKey('t_users.id'))

#     def __repr__(self):
#         return '<ReviewLikes id:{}>'.format(self.review_id)  

#     def __init__(self, data):
#         self.review_id = data['review_id']
#         self.user_id = data['user_id']

# class ReviewUnlikes(db.Model):
#     __tablename__ = 'r_review_unlikes'
#     review_id = db.Column('review_id', db.Integer, db.ForeignKey('t_reviews.id'))
#     user_id = db.Column('user_id', db.Integer, db.ForeignKey('t_users.id'))

#     def __repr__(self):
#         return '<ReviewUnlikes id:{}>'.format(self.review_id)  

#     def __init__(self, data):
#         self.review_id = data['review_id']
#         self.user_id = data['user_id']
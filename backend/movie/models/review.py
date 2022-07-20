from movie import db
from sqlalchemy import *

class Reviews(db.Model):
    __tablename__ = 't_reviews'
    id = db.Column('id', db.String(256), primary_key=True)
    movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('t_movies.id'))
    user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'))
    review_content = db.Column('review_content', db.String(256), nullable=False)
    created_time = db.Column('created_time', db.String(256), nullable=False)
    rating = db.Column('rating', db.Integer, nullable=False)
    weight = db.Column('weight', db.Float(20), nullable=False)
    # relationships
    # review_likes = db.ralationship('ReviewLikes', backref='reviews', lazy=True)
    # review_unlikes = db.relationship('ReviewUnlikes', backref='reviews', lazy=True)
    review_user_likes_rel = db.relationship(
        "Users",
        secondary='r_review_likes',
        back_populates="user_review_likes_rel",
        lazy=True,
        overlaps="review_user_unlikes_rel"
    )

    review_user_unlikes_rel = db.relationship(
        "Users",
        secondary='r_review_unlikes',
        back_populates="user_review_unlikes_rel",
        lazy=True,
        overlaps="review_user_likes_rel"
    )

    def __repr__(self):
        return '<Review id:{}>'.format(self.id)  

    def __init__(self, data):
        self.id = data['id']
        self.movie_id = data['movie_id']
        self.user_id = data['user_id']
        self.review_content = data['review_content']
        self.created_time = data['created_time']
        self.rating = data['rating']
        self.weight = data['weight']

class ReviewLikes(db.Model):
    __tablename__ = 'r_review_likes'
    review_id = db.Column('review_id', db.String(256), db.ForeignKey('t_reviews.id'), primary_key=True)
    user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), primary_key=True)

    def __repr__(self):
        return '<ReviewLikes review id:{} user id: {}>'.format(self.review_id, self.user_id)  

    def __init__(self, data):
        self.review_id = data['review_id']
        self.user_id = data['user_id']

class ReviewUnlikes(db.Model):
    __tablename__ = 'r_review_unlikes'
    review_id = db.Column('review_id', db.String(256), db.ForeignKey('t_reviews.id'), primary_key=True)
    user_id = db.Column('user_id', db.String(256), db.ForeignKey('t_users.id'), primary_key=True)
    def __repr__(self):
        return '<ReviewUnlikes review id:{} user id: {}>'.format(self.review_id, self.user_id)  

    def __init__(self, data):
        self.review_id = data['review_id']
        self.user_id = data['user_id']
from movie import db

follow_relationship = db.Table('follow_relationship',
    db.Column('follower_user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
)

class User(db.Model):

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256))
    posts = db.relationship('Post', back_populates='user', lazy=True)
    collections = db.relationship('Collection', back_populates='user', lazy=True)
    followers = db.relationship('User',
                                secondary=follow_relationship,
                                primaryjoin=user_id==follow_relationship.c.user_id,
                                secondaryjoin=user_id==follow_relationship.c.follower_user_id,
                                backref="followings")
    image = db.Column('image', db.String(256))
    signature = db.Column('signature', db.String(256))
    def __init__(self, username, email, password):
        self.username   = username
        self.email      = email
        self.password   = password

class Post(db.Model):

    __tablename__ = 'post'

    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    content = db.Column(db.String(1024))
    created_time = db.Column(db.Time)
    user = db.relationship("User", back_populates='posts')

    def __init__(self, content):
        self.content = content

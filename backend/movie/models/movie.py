from movie import db

class Movies(db.Model):
    __tablename__ = 't_movies'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title' ,db.String(200), nullable=False)
    tagline = db.Column('tagline', db.String(200))
    backdrop = db.Column('backdrop', db.String(200))
    discription = db.Column('discription', db.String(1000))
    runtime = db.Column('runtime', db.Integer)
    release_time = db.Column('release_time', db.DateTime)
    release_status = db.Column('release_status', db.String(20))
    total_rating = db.Column('total_rating', db.Float(20))
    rating_count = db.Column('rating_count', db.Integer)
    events = db.relationship('Events', secondary='r_event_movie', back_populates='movies', lazy=True)
    movie_director_rel = db.relationship('Persons', secondary='r_movie_director', back_populates='director_movie_rel', lazy=True)
    movie_actor_rel = db.relationship('Persons', secondary='r_movie_actor', back_populates='actor_movie_rel', lazy=True)
    
    def __repr__(self):
        return '<Movie: {} {}>'.format(self.id, self.title)

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.tagline = data['tagline']
        self.backdrop = data['backdrop']
        self.discription = data['discription']
        self.runtime = data['runtime']
        self.release_date = data['release_date']
        self.release_status = data['release_status']
        self.total_rating = data['total_rating']
        self.rating_count = data['rating_count']




class MovieGenres(db.Model):
    __tablename__ = 'Movie_genres'
    genre_id = db.Column('genre_id', db.Integer(20), db.ForeignKey('Genres.id'))
    movie_id = db.Column('movie_id', db.Integer(20), db.ForeignKey('Movies.id'))

    def __repr__(self):
        return '<Movie id: {} genren id: {}>'.format(self.movie_id, self.id)

    def __init__(self, data):
        self.id = data['id']
        self.genre_id = data['genre_id']
        self.movie_id = data['movie_id']

class MovieImages(db.model):
    __tablename__ = 'Movie_images'
    id = db.Column('id', db.Integer(20), primary_key=True)
    movie_id = db.Column('movie_id', db.Integer(20), db.ForeignKey('Movies.id'))
    file_path = db.Column('file_path', db.String(400))
    height = db.Column('height', db.Integer(20))
    width = db.Column('width', db.Integer(20))
    is_posters = db.Column('is_posters', db.Boolean)

    def __repr__(self):
        return '<Images id: {} movie id : {}>'.format(self.id, self.movie_id)

    def __init__(self, data):
        self.id = data['id']
        self.movie_id = data['movie_id']
        self.file_path = data['file_path']
        self.height = data['height']
        self.width = data['width']
        self.is_posters = data['is_posters']
"""
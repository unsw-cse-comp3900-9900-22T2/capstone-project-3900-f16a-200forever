from movie import db

class Movies(db.Model):
    __tablename__ = 't_movies'
    id = db.Column('id', db.Integer(20), primary_key=True)
    title = db.Column('title' ,db.String(200), nullable=False)
    tagline = db.Column('tagline', db.String(200))
    backdrop = db.Column('backdrop', db.String(200))
    discription = db.Column('discription', db.String(1000))
    runtime = db.Column('runtime', db.Integer)
    release_date = db.Column('release_date', db.DateTime)
    release_status = db.Column('release_status', db.String(20))
    total_rating = db.Column('total_rating', db.Float(20))
    rating_count = db.Column('rating_count', db.Integer)

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

class MovieActor(db.model):
    __tablename__ = 'r_movie_actors'
    movie_id = db.Column('movie_id', db.Integer(20), db.ForeignKey('Movies.id'))
    person_id = db.Column('person_id', db.Integer(20), db.ForeignKey('Persons.id'))
    character = db.Column('character', db.String(200))
    order = db.Column('order', db.Integer(20))

    def __repr__(self):
        return '<Movie id: {} actor id: {}>'.format(self.movie_id, self.person_id)

    def __init__(self, data):
        self.movie_id = data['movie_id']
        self.person_id = data['person_id']
        self.character = data['character']
        self.order = data['order']

class MovieDirector(db.model):
    __tablename__ = 'r_movie_directors'
    movie_id = db.Column('movie_id', db.Integer(20), db.ForeignKey('Movies.id'))
    person_id = db.Column('person_id', db.Integer(20), db.ForeignKey('Persons.id'))

    def __repr__(self):
        return '<Movie id: {} director id: {}>'.format(self.movie_id, self.person_id)

    def __init__(self, data):
        self.movie_id = data['movie_id']
        self.person_id = data['person_id']
        

class MoviesGenres(db.Model):
    __tablename__ = 'r_movie_genre'
    genre_id = db.Column('genre_id', db.Integer(20), db.ForeignKey('Genres.id'))
    movie_id = db.Column('movie_id', db.Integer(20), db.ForeignKey('Movies.id'))

    def __repr__(self):
        return '<Movie id: {} genren id: {}>'.format(self.movie_id, self.genre_id)

    def __init__(self, data):
        self.id = data['id']
        self.genre_id = data['genre_id']
        self.movie_id = data['movie_id']

class MovieImages(db.model):
    __tablename__ = 'r_movie_images'
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

class EventMovie(db.Model):
    __tablename__ = 'r_event_movie'
    event_id = db.Column('event_id', db.Integer(20), db.ForeignKey('Events.id'), nullable = False, primary_key = True)
    movie_id = db.Column('movie_id', db.Integer(20), db.ForeignKey('Movies.id'), nullable = False, primary_key = True)

    def __repr__(self):
        return '<EventMovie movie id: {} event id: {}>'.format(self.movie_id, self.event_id)

    def __init__(self, data):
        self.movie_id = data['movie_id']
        self.event_id = data['event_id']

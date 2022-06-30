from ast import keyword
from json import dumps
from flask import Flask
from flask_restx import Resource, reqparse
from flask_restx import Namespace
from tables import Description
from movie import db
from api_movie import MovieNS
from movie.models import movie as Movie
from movie.models import person as Person

movie_ns = MovieNS.movie_ns

# show the details of the movie
@movie_ns.route('/moviedetails')
class MovieDetailController(Resource):
    @movie_ns.response(200, 'Successfully retrieved movie details')
    @movie_ns.response(400, 'Something went wrong')
    def get(self):
        data = movie_ns.payload
        movie_id = data['movie_id']
        select_movie = db.session.query(Movie.Movies).filter(Movie.Movies.id == movie_id).first()
        # genres
        movie_genre_id = db.session.query(Movie.MoviesGenres).filter(Movie.MoviesGenres.movie_id == movie_id).all()
        movie_genre = []
        for i in movie_genre_id:
            genre_id = i['genre_id']
            genre = db.session.query(Movie.Genres).filter(Movie.Genres.id == genre_id).first()['name']
            movie_genre.append(genre)

        if select_movie == None:
            return dumps({'message': 'Cannot find movie'}), 400
        
        # title, backdrop, rating
        movie_title = select_movie['title']
        movie_backdrop = select_movie['backdrop']
        rating_count = select_movie['rating_count']
        total_rating = select_movie['total_rating']
        description = select_movie['description']
        runtime = select_movie['runtime']
        release_time = select_movie['release_time']
        release_status = select_movie['release_status']
        '''
        # if the movie has no rating, set it to -1 which will be displayed as no rating
        if rating_count != 0 and total_rating != 0:
            final_rating = total_rating / rating_count
            final_rating = round(final_rating, 1)
        else:
            final_rating = -1
        '''
        # actors and director
        movie_actors_id = db.session.query(Movie.MovieActor).filter(Movie.MovieActor.movie_id == movie_id).all()
        movie_directors_id = db.session.query(Movie.MovieDirector).filter(Movie.MovieDirector.movie_id == movie_id).all()
        movie_actors = []
        movie_directors = []
        # actors [{'actor_name': sample, 'actor_character': sample}, {}...]
        for i in movie_actors_id:
            actor_id = i['person_id']
            actor_name = db.session.query(Person.Persons).filter(Person.Persons.id == actor_id).first()['name']
            actor_character = i['character']
            movie_actors.append({'actor_name': actor_name, 'actor_character': actor_character})

        # directors [name]
        for i in movie_directors_id:
            director_id = i['person_id']
            director_name = db.session.query(Person.Persons).filter(Person.Persons.id == director_id).first()['name']
            movie_directors.append(director_name)

        movie_details = {
            'id': movie_id, #str
            'name': movie_title, #str
            'backdrop': movie_backdrop, #str
            'description': description, #str
            'runtime': runtime, #int
            'release_time': release_time, #str
            'release_status': release_status, #str
            'total rating': total_rating, #int
            'rating count': rating_count, #int
            'actors': movie_actors, #list of dict
            'directors': movie_directors, #list of str
            'genres': movie_genre,  #list of dict
            'reviews': [] #list of dict
        }
        return dumps(movie_details), 200

        


# enter a keyword and get the list of movies corresponding to the keyword
@movie_ns.route('/search')
class MovieSearchController(Resource):
    @movie_ns.response(200, 'Successfully find movie')
    @movie_ns.response(400, 'Something went wrong')

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', type = str, location = 'args', required = True, help = 'keywords to search')
        args = parser.parse_args()
        keyword = args['keyword']
        if keyword == '':
            return {'message': 'Keyword is empty, please enter again'}, 400

        

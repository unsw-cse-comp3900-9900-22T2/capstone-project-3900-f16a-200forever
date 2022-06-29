from ast import keyword
from flask import Flask
from flask_restx import Resource, reqparse
from flask_restx import Namespace
from movie import db
from api_movie import MovieNs
from movie.models import movie as M

movie_ns = MovieNs.movie_ns

@movie_ns.route('/moviedetails')
class MovieDetailController(Resource):
    @movie_ns.response(200, 'Successfully retrieved movie details')
    @movie_ns.response(400, 'Something went wrong')
    # @movie_ns.response(404, 'Movie not found')
    def get(self):
        data = movie_ns.payload
        movie_id = data['movie_id']
        movie_details = db.session.query(M.Movies).filter(M.Movies.id == movie_id).first()
        if movie_details != None:
            return movie_details.to_dict()
        else:
            return {'message': 'Movie not found'}, 404

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

        

from flask import Flask
from flask_restx import Resource, Api
from flask_restx import Namespace
from movie import db
from api_movie import MovieNs


@MovieNs.route('/moviedetails')
class MovieDetailController(Resource):
    @MovieNs.response(200, 'Successfully retrieved movie details')
    @MovieNs.response(400, 'Something went wrong')
    # @MovieNs.response(404, 'Movie not found')
    def get(self):
        data = MovieNs.payload
        movie_id = data['movie_id']
        movie_details = db.session.query.filter(id == movie_id).first()
        if movie_details != None:
            return movie_details.to_dict()
        else:
            return {'message': 'Movie not found'}, 404

#
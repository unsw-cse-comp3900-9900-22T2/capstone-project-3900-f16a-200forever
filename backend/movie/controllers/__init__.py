from .movie_sys import movie_ns
from flask_restx import Api
from flask import Blueprint

# movie
movie_bp = Blueprint('movie', __name__)
movie_api = Api(movie_bp, version='1.0', title='Movie API', description='Api for movie')
movie_api.add_namespace(movie_ns, path='/movie')
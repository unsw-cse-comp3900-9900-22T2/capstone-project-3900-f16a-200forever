from flask_restx import Namespace

class MovieNs:
    movie_ns = Namespace('Movie', description='Movie related operations')
    
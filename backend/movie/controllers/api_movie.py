from flask_restx import Namespace

class MovieNS:
    movie_ns = Namespace('Movie', description='Movie related operations')

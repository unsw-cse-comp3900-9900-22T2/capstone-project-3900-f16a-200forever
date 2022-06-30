from .auth_sys import auth_ns 
from .admin_sys import admin_ns
from .event_sys import event_ns
from .movie_sys import movie_ns
from .person_sys import person_ns
from flask_restx import Api
from flask import Blueprint

#auth
auth_bp = Blueprint("auth", __name__)
auth_api = Api(auth_bp, version='1.0', title="Auth API", description="Movie Forever api.")
auth_api.add_namespace(auth_ns, path='/') 

#admin 
admin_bp = Blueprint("admin", __name__)
admin_api = Api(admin_bp, version='1.0', title="Admin API", description="Movie Forever api.")
admin_api.add_namespace(admin_ns, path='/admin')

#event
event_bp = Blueprint("event", __name__)
event_api = Api(event_bp, version='1.0', title="Event API", description="Movie Forever api.")
event_api.add_namespace(event_ns, path='/event')


#movie
movie_bp = Blueprint("movie", __name__)
movie_api = Api(movie_bp, version='1.0', title="Movie API", description="Movie Forever api.")
movie_api.add_namespace(movie_ns, path='/movie')

# person
person_bp = Blueprint("person", __name__)
person_api = Api(person_bp, version='1.0', title="Person API", description="Movie Forever api.")
person_api.add_namespace(person_ns, path='/person')
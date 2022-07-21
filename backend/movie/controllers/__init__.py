
import imp
from .auth_sys import auth_ns 
from .admin_sys import admin_ns
from .event_sys import event_ns
from .movie_sys import movie_ns
from .person_sys import person_ns
from .user_sys import user_ns
from .genre_sys import genre_ns
from .review_sys import review_ns
from .recommendation_sys import recommendation_ns
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


#user 
user_bp = Blueprint("user", __name__)
user_api = Api(user_bp, version='1.0', title="User API", description="Movie Forever api.")
user_api.add_namespace(user_ns, path='/user')

# genre 
genre_bp = Blueprint("genre", __name__)
genre_api = Api(genre_bp, version='1.0', title="Genre API", description="Movie Forever api.")
genre_api.add_namespace(genre_ns, path='/genre')

# review
review_bp = Blueprint("review", __name__)
review_api = Api(review_bp, version='1.0', title="Review API", description="Movie Forever api.")
review_api.add_namespace(review_ns, path='/review')

# reconmendation
recommendation_bp = Blueprint("recommendation", __name__)
recommendation_api = Api(recommendation_bp, version='1.0', title="recommendation API", description="Movie Forever api.")
recommendation_api.add_namespace(recommendation_ns, path='/recommendation')

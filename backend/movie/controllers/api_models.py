from attr import field
from flask_restx import Namespace
from .models_format import login, validation, event_create
from numpy import require

class AuthNS:
  auth_ns = Namespace("Auth", description="the api of normal user authentication")
  auth_login = auth_ns.model('Auth Login', login)
  auth_logout = auth_ns.model('Auth logout', validation)

class AdminNS:
  admin_ns = Namespace("Admin", description="the api of admin authentication")

class EventNS:
  event_ns = Namespace('Event', description="the api for manage event")
  event_create_form = event_ns.model('Create event', event_create)
  validation_form = event_ns.model("Validate", validation)
  
class MovieNS:
  movie_ns = Namespace('Movie', description="the api for manage movie")


from attr import field
from flask_restx import Namespace
from .models_format import login, validation, event_detail, register, send_email, reset_password, forgot_password
from numpy import require

class AuthNS:
  auth_ns = Namespace("Auth", description="the api of normal user authentication")
  auth_login = auth_ns.model('Auth Login', login)
  auth_logout = auth_ns.model('Auth logout', validation)
  auth_register = auth_ns.model('Auth register', register)
  auth_send_email = auth_ns.model('Auth Send Email', send_email)
  auth_reset_password = auth_ns.model('Auth reset_password', reset_password)
  auth_forgot_password = auth_ns.model('Auth forgot password', forgot_password)

class AdminNS:
  admin_ns = Namespace("Admin", description="the api of admin authentication")

class EventNS:
  event_ns = Namespace('Event', description="the api for manage event")
  event_create_form = event_ns.model('Create event', event_detail)
  event_edit_form = event_ns.model('Create event', event_detail)
  validation_form = event_ns.model("Validate", validation)
  
class MovieNS:
  movie_ns = Namespace('Movie', description="the api for manage movie")

class PersonNs:
  person_ns = Namespace('Person', description="the api for person")
  
class UserNs:
  user_ns = Namespace('User', escription="the api for user")
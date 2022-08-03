from flask_restx import Namespace
from .models_format import login, validation, event_detail, register, send_email, reset_password, forgot_password, \
  review_post, review_delete, review_admin, review_admin_delete, edit_profile, attemp_event, finish_event, delete_thread, forum_admin, post_thread, \
  comment_react, thread_comment, follow

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
  attemp_event_form = event_ns.model('Attemp Event', attemp_event)
  finish_event_form = event_ns.model('Attemp Event', finish_event)

class MovieNS:
  movie_ns = Namespace('Movie', description="the api for manage movie")

class PersonNS:
  person_ns = Namespace('Person', description="the api for person")
  
class UserNS:
  user_ns = Namespace('User', escription="the api for user")
  follow_form = user_ns.model('Add follow',follow)
  user_edit_profile = user_ns.model('Edit profile', edit_profile)


class GenreNS:
  genre_ns = Namespace('Genre', description="the api for genre")

  
class ReviewNS:
  review_ns = Namespace('Review', description="the api for review")
  validation_check = review_ns.model("Validate", validation)
  review_create_form = review_ns.model('Review Post', review_post)
  review_delete_form = review_ns.model('Review Delete', review_delete)
  review_admin_form = review_ns.model('Review Admin', review_admin)
  review_admin_delete_form = review_ns.model('Review Admin Delete', review_admin_delete)

class RecommendationNS:
  recommendation_ns = Namespace('Recommendation', description="the api for recommendation")
  
class ThreadNS:
  thread_ns = Namespace('Thread', description="the api for thread")
  delete_thread_form = thread_ns.model('Delete thread', delete_thread)
  forum_admin_form = thread_ns.model('Thread admin',forum_admin) 
  post_thread_form = thread_ns.model('Post thread', post_thread)
  comment_react_form = thread_ns.model("React Thread", comment_react)
  thread_comment_form = thread_ns.model('Thread comment', thread_comment)
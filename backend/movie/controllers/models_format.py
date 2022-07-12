from xml.dom.minidom import Element
from attr import field
from flask_restx import fields

login = {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "is_admin": fields.Boolean(required=True)
}

forgot_password = {
  "email": fields.String(required=True),
  "new_password": fields.String(required=True),
  "confirm_new_password": fields.String(required=True),
  "validation_code": fields.String(required=True),
}

reset_password = {
    "email": fields.String(required=True),
    "new_password": fields.String(required=True),
    "validation_code": fields.String(required=True),
}

validation = {
  'email': fields.String(required=True),
  'token': fields.String(required=True)
}
send_email = {
  'email': fields.String(required=True)
}

register = {
  'name': fields.String(required=True),
  'email': fields.String(required=True),
  'password': fields.String(required=True)
}

attemp_event = {
  'email': fields.String(required=True),
  'token': fields.String(required=True),
  'event_id': fields.String(required=True)
}

finish_event = {
  'email': fields.String(required=True),
  'token': fields.String(required=True),
  'event_id': fields.String(required=True),
  'answers': fields.Raw()
}

delete_thread = {
  'thread_id': fields.String(required=True),
  'email': fields.String(required=True),
  'token': fields.String(required=True)
}

forum_admin = {
  'user_email': fields.String(required=True),
  'admin_email': fields.String(required=True),
  'token': fields.String(required=True)
}

post_thread = {
  'email': fields.String(required=True), 
  'token': fields.String(required=True), 
  'genre_id': fields.Integer(required=True),
  'is_anonymous': fields.Integer(required=True),
  'title': fields.String(required=True), 
  'content': fields.String(required=True)
}

add_follow = {
  'email': fields.String(required=True), 
  'token': fields.String(required=True), 
  'follow_email': fields.String(required=True)
}

class Question_Form(fields.Raw):
  def format(self, value):
    return {  
      'id': fields.String(required=True),
      'content': fields.String(required=True),
      'choice_1': fields.String(required=True),
      'choice_2': fields.String(required=True),
      'choice_3': fields.String(required=True),
      'correct_answer': fields.Integer(required=True),
      }

#TODO: check the required
event_detail = {
  'email': fields.String(required=True),
  'token': fields.String(required=True),
  'topic': fields.String(required=True),
  'duration': fields.Integer(required=True),
  'deadline': fields.DateTime(required=True),
  'image': fields.String(required=True),
  'image_description': fields.String(required=True),
  'description': fields.String(required=True),
  'require_correctness_amt': fields.Integer(required=True),
  'questions': fields.List(Question_Form(required=True)), 
  'movies': fields.List(fields.Integer, required=True)
}
"""
user_profile = {
  'id': fields.String(required=True),
  'username': fields.String(required=True),
  'p'
}
"""

    
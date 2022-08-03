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
  'answers': fields.Raw(required=True)
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

follow = {
  'email': fields.String(required=True), 
  'token': fields.String(required=True), 
  'follow_id': fields.String(required=True),
  "page_num": fields.Integer(required=True),
  "num_per_page": fields.Integer(required=True)
}

class Question_Form(fields.Raw):
  def format(self, value):
    return {  
      'id': fields.String(),
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

# Accept null values
class NullableString(fields.String):
    __schema_type__ = ['string', 'null']
    __schema_example__ = 'nullable string'


edit_profile = {
  'username': fields.String(required=True),
  'signature': fields.String,
  'image': fields.String,
  'current_password': fields.String,
  'new_password': fields.String,
  'double_check': fields.String,
  'email': fields.String(required=True),
  'token': fields.String(required=True)
}

review_post = {
  'email': fields.String(required=True),
  'token': fields.String(required=True),
  'movie_id': fields.Integer(required=True),
  'rating': fields.Integer(required=True),
  'review_content': fields.String(required=True)
}

review_delete = {
  'email': fields.String(required=True),
  'token': fields.String(required=True),
  'review_id': fields.String(required=True)
}

review_admin = {
  'user_email': fields.String(required=True),
  'admin_email': fields.String(required=True),
  'token': fields.String(required=True)
}

review_admin_delete = {
  'user_email': fields.String(required=True),
  'token': fields.String(required=True),
  'movie_id': fields.Integer(required=True),
  'admin_email': fields.String(required=True)
}

comment_react = {
  'email': fields.String(required=True),
  'token': fields.String(required=True),
  "comment_id": fields.String(required=True)
}


thread_comment = {
  "email": fields.String(required=True),
  'token': fields.String(required=True),
  "content": fields.String(required=True),
  "thread_id": fields.String(required=True),
  "is_anonymous": fields.Integer,
  "reply_comment_id": fields.String
}
from flask_restx import fields

login = {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'is_admin': fields.Boolean(required=True)
}


logout = {
  'email': fields.String(required=True),

}

class Question_Form(fields.Raw):
  def format(self, value):
    return {
      'content': fields.String(required=True),
      'choice_1': fields.String(required=True),
      'choice_2': fields.String(required=True),
      'choice_3': fields.String(required=True),
      'correct_answer': fields.Integer,
      }

#TODO: check the required
event_create = {
  'topic': fields.String(required=True),
  'duration': fields.Integer(required=True),
  'deadline': fields.DateTime(required=True),
  'image': fields.String(required=True),
  'image_description': fields.String(required=True),
  'description': fields.String(required=True),
  'require_correctness_amt': fields.Integer(required=True),
  'questions': fields.List(Question_Form(required=True))
}

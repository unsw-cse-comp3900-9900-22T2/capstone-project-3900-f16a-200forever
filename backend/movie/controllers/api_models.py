from flask_restx import Namespace, fields
from numpy import require

class AuthNS:
  auth_ns = Namespace("Auth", description="TODO")
  auth_login = auth_ns.model('Auth Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
  })
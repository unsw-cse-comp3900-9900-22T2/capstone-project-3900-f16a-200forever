from flask_restx import Namespace, fields
from numpy import require

login = {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'is_admin': fields.Boolean(required=True)
}


logout = {
  'email': fields.String(required=True),

}

class AuthNS:
  auth_ns = Namespace("Auth", description="the api of normal user authentication")
  auth_login = auth_ns.model('Auth Login', login)

  auth_logout = auth_ns.model('Auth logout', logout)


class AdminNS:
  admin_ns = Namespace("Admin", description="the api of admin authentication")
  admin_login = admin_ns.model('Admin login', login)

  admin_logout = admin_ns.model('Admin logout', logout)
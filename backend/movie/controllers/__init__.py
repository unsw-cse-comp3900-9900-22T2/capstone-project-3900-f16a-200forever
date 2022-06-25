from .authController import auth_ns 
from flask_restx import Api
from flask import Blueprint

#auth
auth_bp = Blueprint("auth", __name__)
auth_api = Api(auth_bp, version='1.0', title="Auth API", description="Movie Forever api.")
auth_api.add_namespace(auth_ns, path='/auth')


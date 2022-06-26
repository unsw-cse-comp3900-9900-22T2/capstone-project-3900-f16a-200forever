from .authController import auth_ns 
from .adminController import admin_ns
from .eventController import event_ns
from flask_restx import Api
from flask import Blueprint

#auth
auth_bp = Blueprint("auth", __name__)
auth_api = Api(auth_bp, version='1.0', title="Auth API", description="Movie Forever api.")
auth_api.add_namespace(auth_ns, path='/auth')

#admin 
admin_bp = Blueprint("admin", __name__)
admin_api = Api(admin_bp, version='1.0', title="Admin API", description="Movie Forever api.")
admin_api.add_namespace(admin_ns, path='/admin')

#event
event_bp = Blueprint("event", __name__)
event_api = Api(event_bp, version='1.0', title="Event API", description="Movie Forever api.")
event_api.add_namespace(event_ns, path='/event')

from importlib.resources import Resource
from .api_models import AdminNS
from flask_restx import Resource, reqparse
from movie import db

from movie.models import admins
from movie.utils.auth_util import generate_token, pw_encode
from flask import session
from json import dumps

admin_ns = AdminNS.admin_ns


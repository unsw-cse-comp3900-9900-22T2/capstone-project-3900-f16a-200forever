
from movie.models import *
from movie import db
from flask import session

db.create_all()
db.session.commit()


import imp
from numpy import require
from .api_models import PersonNs
from flask_restx import Resource, reqparse
from movie.models import person as Person
from movie import db
from movie.utils.other_until import convert_object_to_dict
from movie.utils.person_until import get_gender
from json import dumps

person_ns = PersonNs.person_ns

@person_ns.route("/detail")
class PersonDetail(Resource):
  @person_ns.response(200, "Successfully")
  @person_ns.response(400, "Something wrong")
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str, location='args', required=True)
    args = parser.parse_args()
    id = args['id']

    # get the person
    person = db.session.query(Person.Persons).filter(Person.Persons.id == id).first()

    if person == None:
      return {"message": f"Person {id} not found"}
    data = convert_object_to_dict(person)
    data["gender"] = get_gender(data["gender"])
    return data, 200

from .api_models import PersonNS
from flask_restx import Resource, reqparse
from movie.models import person as Person
from movie import db
from movie.utils.other_util import convert_object_to_dict
from movie.utils.person_util import get_gender

person_ns = PersonNS.person_ns

#----------------PERSON DETAIL------------------
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
      return {"message": f"Person of id = {id} do not exist"}, 400
    data = convert_object_to_dict(person)
    data["gender"] = get_gender(data["gender"])
    return data, 200

from datetime import datetime

from app.udaconnect.models import Person, Location, Connection
from app.udaconnect.schemas import PersonSchema, ConnectionSchema
from app.udaconnect.services import personService, connectionService

from flask import request, jsonify
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect Person", description="Provides person data.")  # noqa

@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    @api.doc(description='Insert a new person into Database')
    def post(self):
        try:
            payload = request.get_json()
            personService.create(payload)
            return {'status': 'success'}, 202
        except:
            return {'error':'error in personService POST Request'}, 400        

    @responds(schema=PersonSchema, many=True)
    @api.doc(description='Retrieve and list existing people from Database')
    def get(self) -> List[Person]:
        try:
            persons: List[Person] = personService.retrieve_all()
            return persons
        except:
            return {'error':'error in personService GET Request'}, 400        


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    @api.doc(description='Retrieve a person with given ID from Database')
    def get(self, person_id) -> Person:
        try:
            person: Person = personService.retrieve(person_id)
            return person
        except:
            return jsonify({'error':'error in personService GET ID Request'}), 400        


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
@api.doc(description='Search for connection data for a given person_id')
class connectionResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> List[ConnectionSchema]:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(
            request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        results = connectionService.find_contacts(
            person_id=int(person_id),
            start_date=start_date,
            end_date=end_date,
            meters=float(distance)
        )

        connection_list: List[Connection] = [
            connectionResource.pb2_to_model(connection)
            for connection in results.connections
        ]

        return connection_list

    @staticmethod
    def pb2_to_model(connection) -> Connection:
        location_pb2 = connection.location
        location = Location(id=location_pb2.id,
                            person_id=location_pb2.person_id,
                            wkt_shape=location_pb2.wkt_shape,
                            creation_time=datetime.fromtimestamp(
                                location_pb2.creation_time.seconds)
                            )

        person_pb2 = connection.person
        person = Person(id=person_pb2.id,
                        first_name=person_pb2.first_name,
                        last_name=person_pb2.last_name,
                        company_name=person_pb2.company_name)

        return Connection(person=person, location=location)

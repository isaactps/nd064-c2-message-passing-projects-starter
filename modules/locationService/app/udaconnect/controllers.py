from datetime import datetime

from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services import locationService

from flask import request, jsonify
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect Location", description="Provides location data.")  # noqa

@api.route("/locations")
class LocationsResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    @api.doc(description='Insert a new location into Database')    
    def post(self):
        try:
            payload = request.get_json()
            locationService.create(payload)
            return {'status': 'success'}, 202
        except:
            return {'error':'error in locationService POST Request'}, 400        

    @responds(schema=LocationSchema, many=True)
    @api.doc(description='Retrieve and list existing locations from Database')
    def get(self) -> List[Location]:
        try:
            locations: List[Location] = locationService.retrieve_all()
            return locations
        except:
            return {'error':'error in locationService GET Request'}, 400        
                

@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query") 
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    @api.doc(description='Retrieve a location with given ID from Database')    
    def get(self, location_id) -> Location:
        try: 
            location: Location = locationService.retrieve(location_id)
            return location
        except:
            return jsonify({'error':'error in locationService GET [ID] Request'}), 400        
    

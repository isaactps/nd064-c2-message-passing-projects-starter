import logging

from datetime import datetime, timedelta
from typing import Dict, List

from builtins import staticmethod

from app import db
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.kafkaMessage import locationProducer

from sqlalchemy.sql import text

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("locationService-api")

class locationService:
    @staticmethod
    def create(location: Dict):
        locationProducer.send_message(location) #Sending to Kafka Topic
        
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def retrieve_all() -> List[Location]:
        return db.session.query(Location).all()        

import logging

from geoalchemy2.functions import ST_Point
from datetime import datetime, timedelta
from typing import Dict, List

from app.udaconnect.models import Person, Location
from app.udaconnect.schemas import PersonSchema, LocationSchema
from app.udaconnect.config import DBSession

from sqlalchemy.sql import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("locationConsumer")

session = DBSession()

class locationService:
    @staticmethod
    def create(location: Dict):
        """
        Inject a location data model to DB.

        :param location: A location dict
        """    

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        
        session.add(new_location)
        session.commit()

        logger.info(f"New location injected: {new_location.id}")
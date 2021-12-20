import logging

from datetime import datetime, timedelta
from typing import Dict, List

from app.udaconnect.models import Person
from app.udaconnect.schemas import PersonSchema
from app.udaconnect.config import DBSession

from sqlalchemy.sql import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("personConsumer")

session = DBSession()

class personService:
    @staticmethod
    def create(person: Dict) -> Person:
        """
        Inject a person data model to DB.

        :param person: A Person dict
        """    
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        session.add(new_person)
        session.commit()

        logger.info(f"New person injected: {new_person.id}")

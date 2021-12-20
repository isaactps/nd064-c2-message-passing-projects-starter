import grpc
import logging

from datetime import datetime, timedelta
from typing import Dict, List

from builtins import staticmethod
from google.protobuf.timestamp_pb2 import Timestamp

from app import db
from app.udaconnect.models import Person
from app.udaconnect.schemas import PersonSchema
from app.udaconnect.kafkaMessage import personProducer
from app.udaconnect.connectionService_pb2_grpc import connectionServiceStub
from app.udaconnect.connectionService_pb2 import searchMessage

from sqlalchemy.sql import text

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("personService-api")

channel = grpc.insecure_channel("udaconnect-connection-service:5005")
stub = connectionServiceStub(channel)

class personService:
    @staticmethod
    def create(person: Dict):
        personProducer.send_message(person) #Sending to Kafka Topic

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()


class connectionService:

    @staticmethod
    def find_contacts(person_id, start_date, end_date, meters):

        ts_start = Timestamp(seconds=int(start_date.timestamp()))
        ts_end = Timestamp(seconds=int(end_date.timestamp()))

        search_msg = searchMessage(person_id=person_id,
                                   start_date=ts_start,
                                   end_date=ts_end,
                                   meters=meters)

        response = stub.FindConnections(search_msg)

        return response

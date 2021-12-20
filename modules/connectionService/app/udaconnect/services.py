from datetime import datetime, timedelta
from typing import List

from app.udaconnect.config import DBSession, engine
from app.udaconnect.connectionService_pb2 import Person as PersonPB2, Location as LocationPB2, connectionMessage, connectionMessageList
from app.udaconnect.models import Person
from app.udaconnect.models import Location

from google.protobuf.timestamp_pb2 import Timestamp

from sqlalchemy.sql import text

session = DBSession()

class connectionService:

    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime,
                      meters=5) -> connectionMessageList:
        """
        Finds all Person who have been within a given distance of a given
        Person within a date range.

        :param person_id: Person id to look for contacts
        :param start_date: The start date for looking for contacts
        :param end_date: The end date for looking for contacts
        :param meters: The distance to check for proximity. Default: 5
        """

        locations: List = locationService.fetch_locations(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date
        )

        # Prepare arguments for queries
        data = []
        for location in locations:
            f_end_date = (end_date + timedelta(days=1)).strftime("%Y-%m-%d")
            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": f_end_date,
                }
            )

        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate),
                ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography,:meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )

        connection_list = connectionMessageList()
        result: List[connectionMessage] = []
        for line in tuple(data):
            for (
                    exposed_person_id,
                    location_id,
                    exposed_lat,
                    exposed_long,
                    exposed_time,
            ) in engine.execute(query, **line):
                location = LocationPB2(
                    id=location_id,
                    person_id=exposed_person_id,
                    creation_time=Timestamp(
                        seconds=int(exposed_time.timestamp())
                    ),
                )
                location.wkt_shape = f"ST_POINT({exposed_lat} {exposed_long})"

                result.append(
                    connectionMessage(
                        person=connectionService.person_to_pb2(
                            personService.retrieve(exposed_person_id)
                        ), location=location
                    )
                )

        connection_list.connections.extend(result)

        return connection_list

    @staticmethod
    def person_to_pb2(person) -> PersonPB2:
        """
        Convenience method for translating a Person model do a Protobuf Person.
        :param person: Person model to convert
        :return: PersonPB2
        """

        return PersonPB2(id=person.id, first_name=person.first_name,
                         last_name=person.last_name,
                         company_name=person.company_name)


class personService:
    @staticmethod
    def retrieve_all() -> List[Person]:
        return session.query(Person).all()

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = session.query(Person).get(person_id)
        return person


class locationService:

    @staticmethod
    def fetch_locations(person_id, start_date, end_date) -> List:
        """
        Fetch locations for a person_id given a range of time.

        :param person_id: The person id to look for
        :param start_date: Start date (inclusive)
        :param end_date: End date (exclusive)
        :return: List
        """

        locations: List = session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()

        return locations


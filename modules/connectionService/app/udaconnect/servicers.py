import logging
from datetime import datetime

from app.udaconnect.connectionService_pb2_grpc import connectionServiceServicer
from app.udaconnect.services import connectionService

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("connectionService")

class connectionServicer(connectionServiceServicer):

    def FindConnections(self, request, context):
        """

        Endpoint for searching connection data between selected person_id
        and other that shared a close geo proximity.

        :param request: SearchMessage request data for finding connections
        :param context: gRPC context
        :return: Returns a ConnectionMessageList containing ConnectionMessage
        instances found
        """

        params = {
            'start_date': datetime.fromtimestamp(request.start_date.seconds),
            'end_date': datetime.fromtimestamp(request.end_date.seconds),
            'person_id': int(request.person_id),
            'meters': float(request.meters)
        }

        connection_list = connectionService.find_contacts(**params)

        return connection_list

import os
import time
import logging
from concurrent import futures

import grpc

from app.udaconnect.servicers import connectionServicer
from app.udaconnect.connectionService_pb2_grpc import add_connectionServiceServicer_to_server

SERVER_HOST = os.environ.get('HOST') or 'localhost'
SERVER_PORT = 5005

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("connectionService")

def grpc_serve():
    """Start grpc server servicing FMS RPCs."""
    # Create grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

    # Add service
    add_connectionServiceServicer_to_server(connectionServicer(), server)

    # Start server
    address = '%s:%s' % (SERVER_HOST, SERVER_PORT)
    
    logger.info('Server starting on port {SERVER_PORT}')
    server.add_insecure_port('[::]:{}'.format(SERVER_PORT))
    server.start()

    # Mark server as healthy
    logging.info('grpc listening at %s', address)

    # Start() does not block so sleep-loop
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    grpc_serve()
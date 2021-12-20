import grpc
import os
import sys

from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

from app.udaconnect.connectionService_pb2_grpc import connectionServiceStub
from app.udaconnect.connectionService_pb2 import searchMessage

if __name__ == '__main__':

    grpc_host = os.environ.get('GRPC_HOST') or 'localhost:30003'

    channel = grpc.insecure_channel(grpc_host)
    stub = connectionServiceStub(channel)
    
    start_date = [2020, 1, 1]
    end_date = [2020, 12, 30]
    person_id = 6
    distance = 10

    t_start = datetime(year=int(start_date[0]), month=int(start_date[1]), day=int(start_date[2]))
    t_end = datetime(year=int(end_date[0]), month=int(end_date[1]), day=int(end_date[2]))

    ts_start = Timestamp(seconds=int(t_start.timestamp()))
    ts_end = Timestamp(seconds=int(t_end.timestamp()))

    search_msg = searchMessage(person_id=person_id,
                               start_date=ts_start,
                               end_date=ts_end,
                               meters=distance)

    print(f"Search Person Input: {search_msg}")

    response = stub.FindConnections(search_msg)

    print(f"Response: {response}")

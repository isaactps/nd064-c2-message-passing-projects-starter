import json
import logging
import threading

from app.udaconnect.services import personService
from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("personConsumer")

KAFKA_SERVER = 'kafka:9092'
TOPIC_NAME = 'person'

class personConsumer(threading.Thread):
    """
    Non blocking kafka consumer.
    Base on kafka-python examples @
    https://github.com/dpkp/kafka-python/blob/master/example.py
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        logger.info('Starting personConsumer service')

#        consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER, group_id=None)
        kafka_consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER,
                                 consumer_timeout_ms=1000,
                                 group_id='person-group')
        kafka_consumer.subscribe([TOPIC_NAME])

        while not self.stop_event.is_set():
            for message in kafka_consumer:
                personService.create(json.loads(message.value.decode('utf-8')))
                if self.stop_event.is_set():
                    break

        logger.info('Stopping personConsumer service')
        kafka_consumer.close()

import json
import logging

from kafka import KafkaProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("locationService-api")

KAFKA_SERVER = 'kafka:9092'
TOPIC_NAME = 'location'

kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

class locationProducer:
    def delivery_callback(err, msg):
        if err:
            logger.err('Message delivery failed')
        else:
            logger.info('Message was successfully delivered')

    @staticmethod
    def send_message(location):
        """
        Produces message to Kafka location creation topic

        :param location: Location
        :param location: Location data to send
        :return:
        """
        #kafka_producer.send(TOPIC_NAME, json.dumps(location).encode('utf-8'), callback=delivery_callback(err, msg))
        #kafka_producer.poll(0)
        kafka_producer.send(TOPIC_NAME, json.dumps(location).encode('utf-8'))
        kafka_producer.flush(timeout=5.0)
        

import json
import logging

from kafka import KafkaProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("personService-api")

KAFKA_SERVER = 'kafka:9092'
TOPIC_NAME = 'person'

kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

class personProducer:

    def delivery_callback(err, msg):
        if err:
            logger.err('Message delivery failed')
        else:
            logger.info('Message was successfully delivered')

    @staticmethod
    def send_message(person):
        """
        Produces message to Kafka person creation topic

        :param person: Person
        :param person: Person data to send
        :return:
        """
        #kafka_producer.send(TOPIC_NAME, json.dumps(person).encode('utf-8'), callback=delivery_callback(err, msg))
        #kafka_producer.poll(0)
        kafka_producer.send(TOPIC_NAME, json.dumps(person).encode('utf-8'))
        kafka_producer.flush(timeout=5.0)

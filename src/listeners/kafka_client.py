"""

"""
import json

from kafka import KafkaProducer

from src.listeners import CreateSingleton
from main import logger


# handle exception


def str_to_binary(the_str):
    encoded_str = the_str.encode('ascii')
    return encoded_str


def dict_to_binary(the_dict):
    encoded_str = json.dumps(the_dict)
    binary = ' '.join(format(ord(letter), 'b') for letter in encoded_str)
    return binary


class KafkaPublish(metaclass=CreateSingleton):
    """

    """

    def __init__(self, config):
        """

        :param config:
        """
        try:
            self.config = config
            if self.config.enable_queue:
                self.alert_topic = config.kafka_alerts_topic
                self.publisher = KafkaProducer(
                    bootstrap_servers=config.kafka_host,
                    # value_serializer=lambda m: json.dumps(m).encode('ascii'),
                    # compression_type='gzip',
                    # retries=3,
                    # acks=1
                )
            else:
                self.publisher = {
                    "Kafka_queues": "Disabled",
                    "message": "Currently working in API mode Set queues to true in config"}
        except Exception as e:
            logger.exception(e)
            raise

    def on_send_success(self, record_metadata):
        logger.debug('Success Callback on Publish[%s:%s]' % (record_metadata.topic, record_metadata.offset))

    def on_send_error(self, excp):
        logger.error('Error callback on publish', exc_info=excp)

    def publish(self, payload):
        """

        :param payload:
        :return:
        """
        if self.config.enable_queue:
            try:
                logger.debug("Publishing to topic[%s] message[%s] " % (self.alert_topic, payload))
                resp = self.publisher.send(
                    self.alert_topic,
                    b"hello",
                ).add_callback(self.on_send_success).add_errback(self.on_send_error)
                return resp.__dict__
            except Exception as e:
                logger.exception(e)
                return e
        else:
            return self.publisher

    def close(self):
        """

        :return:
        """
        try:
            if self.config.enable_queue:
                self.publisher.flush(timeout=5)
                self.publisher.close()
        except Exception as e:
            logger.error(e)
        logger.debug("Closed Kafka connection pool")

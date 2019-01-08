"""

"""
import json

from kafka import KafkaProducer

from src.listeners import CreateSingleton
from utilities import logger


def on_send_success(record_metadata):
    logger.debug('Success Callback on Publish[%s:%s]' % (record_metadata.topic, record_metadata.offset))


def on_send_error(excp):
    logger.error('Error callback on publish', exc_info=excp)
    # handle exception


class KafkaPublish(metaclass=CreateSingleton):
    """

    """

    def __init__(self, config):
        """

        :param config:
        """
        try:
            self.alert_topic = config.kafka_alerts_topic
            self.publisher = KafkaProducer(
                bootstrap_servers=config.kafka_host,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                compression_type='gzip',
                retries=3
            )
        except Exception as e:
            logger.error(e)
            raise

    def publish(self, payload):
        """

        :param payload:
        :return:
        """
        try:
            fut = self.publisher.send(
                topic=self.alert_topic,
                value=payload
            ).add_callback(on_send_success).add_errback(on_send_error)
            resp = fut.__dict__
        except Exception as e:
            logger.error(e)
            resp = e
        return resp

    def close(self):
        """

        :return:
        """
        logger.info("Closing Kafka connection pool")
        self.publisher.flush()
        self.publisher.close()

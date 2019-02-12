#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
import logging

from aiokafka import AIOKafkaProducer

from src.listeners import CreateSingleton
from utilities import logger


# handle exception


def str_to_binary(the_str):
    encoded_str = the_str.encode('ascii')
    return encoded_str


def dict_to_binary(the_dict):
    encoded_str = json.dumps(the_dict)
    binary = ' '.join(format(ord(letter), 'b') for letter in encoded_str)
    return binary


class LogFactory(logging.Handler, metaclass=CreateSingleton):
    """
    siege -c50 -t10S -b --content-type "application/json" 'http://localhost:8001/incoming/queue POST { "pay_key":"pay_value"}
    """

    def __init__(self, config, loop):
        """

        :param config:
        """
        logging.Handler.__init__(self)
        try:
            self.config = config
            if self.config.enable_queue:
                self.alert_topic = config.kafka_alerts_topic
                self.publisher = AIOKafkaProducer(bootstrap_servers=self.config.kafka_host,
                                                  client_id="Grata",
                                                  value_serializer=lambda m: json.dumps(m).encode('ascii'),
                                                  loop=loop,
                                                  enable_idempotence=True
                                                  )
                self.publisher.start()
                asyncio.ensure_future(self.publisher.start())

            else:
                self.publisher = {
                    "Kafka_queues": "Disabled",
                    "message": "Currently working in API mode, set queues to True in config"}
        except Exception as e:
            logger.exception(e, exc_info=True)
            asyncio.get_event_loop().close()

    def emit(self, payload):
        if 'kafka.' in payload.name:
            return
        try:
            msg = self.format(payload)
            self.publisher.send(self.alert_topic, {"log": msg, "source": "Grata"})
            asyncio.ensure_future(self.publisher.send(self.alert_topic, {"log": msg, "source": "Grata"}))
        except Exception:
            logging.Handler.handleError(self, payload)

    def flush(self, timeout=None):
        """Flush the objects."""
        self.producer.flush(timeout=timeout)
        asyncio.ensure_future(self.publisher.flush())

    def close(self):
        """Close the producer and clean up."""
        self.acquire()
        try:
            if self.producer:
                self.producer.stop()
                asyncio.ensure_future(self.publisher.stop())
            logging.Handler.close(self)
        finally:
            self.release()

# -*- coding: utf-8 -*-
"""Module to provide kafka handlers for internal logging facility."""
import json_logging

import json
import logging
import sys

from kafka import KafkaProducer


class Config:
    """

    """

    def __init__(self, config: dict):
        """

        :param config:
        """
        for key, value in config.items():
            setattr(self, key, value)


async def __routes_list_filter__(app, url_filter="/"):
    """

    :param app:
    :param url_filter:
    :return:
    """
    map_routes = {}
    for patterns in app.routes:
        decoded_pattern = patterns.simplified_pattern.decode("utf-8")
        handler_str = str("%s::%s" % (sys.modules[patterns.handler.__module__].__name__,
                                      patterns.handler.__name__))
        if (decoded_pattern.startswith(url_filter) and
                decoded_pattern != url_filter and
                decoded_pattern != url_filter + "/" and not
                handler_str.startswith("src.server") and
                decoded_pattern.endswith("/")):
            unpack_method_list = []
            for unpack_methods in list(patterns.methods):
                unpack_method_list.append(unpack_methods.decode("utf-8"))

            map_routes[decoded_pattern] = dict(methods=unpack_method_list,
                                               params=patterns.params_book,
                                               handler=handler_str.replace("src.handlers.", ""))
    return map_routes


class KafkaHandler(logging.Handler):
    """Class to instantiate the kafka logging facility."""

    def __init__(self, hostlist, topic='infrastructure', tls=None):
        """Initialize an instance of the kafka handler."""
        logging.Handler.__init__(self)
        self.producer = KafkaProducer(bootstrap_servers=hostlist,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                      linger_ms=10)
        self.topic = topic

    def emit(self, record):
        """Emit the provided record to the kafka_client producer."""
        # drop kafka logging to avoid infinite recursion
        if 'kafka.' in record.name:
            return

        try:
            # apply the logger formatter
            msg = self.format(record)
            self.producer.send(self.topic, {'message': msg})
            self.flush(timeout=1.0)
        except Exception:
            logging.Handler.handleError(self, record)

    def flush(self, timeout=None):
        """Flush the objects."""
        self.producer.flush(timeout=timeout)

    def close(self):
        """Close the producer and clean up."""
        self.acquire()
        try:
            if self.producer:
                self.producer.close()

            logging.Handler.close(self)
        finally:
            self.release()


json_logging.ENABLE_JSON_LOGGING = True
json_logging.COMPONENT_NAME="Grata"
json_logging.init()
logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
kh = KafkaHandler(['logs.limetray.infra:9092'], 'infrastructure')
logger.addHandler(kh)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info("Kafka Logger Initialized")

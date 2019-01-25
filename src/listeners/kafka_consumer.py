#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json

from aiokafka import AIOKafkaConsumer

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


class KafkaConsumer(metaclass=CreateSingleton):
    """
    siege -c50 -t10S -b --content-type "application/json" 'http://localhost:8001/incoming/queue POST { "pay_key":"pay_value"}
    """

    def __init__(self, config, loop):
        """

        :param config:
        """
        try:
            self.config = config
            if self.config.enable_queue:
                self.alert_topic = config.kafka_alerts_topic
                self.consumer = AIOKafkaConsumer(self.alert_topic,
                                                 bootstrap_servers=self.config.kafka_host,
                                                 client_id="GrataL",
                                                 loop=loop,
                                                 group_id="reports_listener",
                                                 metadata_max_age_ms=5000)

                self.consumer.start()
                asyncio.ensure_future(self.consumer.start())

            else:
                self.consumer = {
                    "Kafka_queues": "Disabled",
                    "message": "Currently working in API mode, set queues to True in config"}
        except Exception as e:
            logger.exception(e, exc_info=True)
            asyncio.get_event_loop().close()

    async def consume(self):

        if self.config.enable_queue:
            try:
                logger.debug("Publishing to topic[%s] message[%s] " % (self.alert_topic, payload))
                send_future = await self.publisher.send(self.alert_topic, {"msg": payload, "source": "Grata"})
                # await asyncio.sleep(1)
                logger.debug(await send_future)
                return send_future
            except Exception as Kaf:
                print(Kaf)
                logger.exception("Catching Exception %s" % Kaf, exc_info=True)

        else:
            return self.consumer

    def close(self):
        """

        :return:
        """
        try:
            if self.config.enable_queue:
                self.publisher.flush()
                self.publisher.stop()
                asyncio.ensure_future(self.publisher.flush())
                asyncio.ensure_future(self.publisher.stop())
                logger.debug("Closed Kafka connection pool")
        except Exception as e:
            logger.error(e)
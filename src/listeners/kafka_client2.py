#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json

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


class KafkaPublish(metaclass=CreateSingleton):
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
                self.publisher = AIOKafkaProducer(bootstrap_servers=self.config.kafka_host,
                                                  client_id="Grata",
                                                  value_serializer=lambda m: json.dumps(m).encode('ascii'),
                                                  loop=loop,
                                                  enable_idempotence=True
                                                  )
                self.publisher.start()
                asyncio.ensure_future(self.publisher.start())
                # print(self.publisher.client.hosts)
                # print(self.publisher.client.fetch_all_metadata())
                # asyncio.ensure_future(self.publisher.client.fetch_all_metadata())
                # print(self.publisher._metadata)

            else:
                self.publisher = {
                    "Kafka_queues": "Disabled",
                    "message": "Currently working in API mode, set queues to True in config"}
        except Exception as e:
            logger.exception(e,exc_info=True)
            asyncio.get_event_loop().close()

    async def publish(self, payload):

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
            # except KafkaTimeoutError:
            #     print("produce timeout... maybe we want to resend data again?")
            # except KafkaError as err:
            #     print("some kafka error on produce: {}".format(err))
        else:
            return self.publisher

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


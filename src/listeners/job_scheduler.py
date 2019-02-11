#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

import aiojobs

from src.listeners import CreateSingleton
from utilities import logger


class Scheduler(metaclass=CreateSingleton):
    """

    """

    def __init__(self):
        """

        """
        try:
            self.scheduler = aiojobs.create_scheduler(close_timeout=30)
        except Exception as e:
            logger.exception(e, exc_info=True)
            asyncio.get_event_loop().close()

    async def spawn_job(self,func):
        try:
            resp = await self.scheduler.spawn(func)
            return resp
        except Exception as e:
            logger.exception(e, exc_info=True)

    def close(self):
        """

        :return:
        """
        try:
            self.scheduler.close()
        except Exception as e:
            logger.exception(e, exc_info=True)

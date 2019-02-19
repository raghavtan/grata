#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

from aioelasticsearch import Elasticsearch

from src.listeners import CreateSingleton
from utilities import logger


class EsClient(metaclass=CreateSingleton):
    """
    siege -c50 -t10S -b --content-type "application/json" 'http://localhost:8001/incoming/queue POST { "pay_key":"pay_value"}
    """

    def __init__(self, config):
        """

        :param config:
        """
        try:
            self.es = Elasticsearch(hosts=config.eshost, loop=asyncio.get_event_loop())
            self.indices = self.es.indices.get('*')
            logger.info("Initializing ES connection")

        except Exception as e:
            logger.exception(e, exc_info=True)
            asyncio.get_event_loop().close()

    def query_builder(self, match_term, ignore_term,since):
        ignore_term_list = []
        for ignore in ignore_term:
            ignore_dict = {
                "term": {
                }
            }

            k, v = next(iter(ignore.items()))
            ignore_dict["term"][k] = v
            ignore_term_list.append(
                ignore_dict
            )

        match_term_list = []
        for match in match_term:
            match_dict = {
                "term": {
                }
            }
            k, v = next(iter(match.items()))
            match_dict["term"][k] = v
            match_term_list.append(
                match_dict
            )
        base = {
            "query": {
                "bool": {
                    "filter": {
                        "bool": {
                            "must": match_term_list,
                            "must_not": ignore_term_list
                        }
                    },
                    "must": {
                        "range": {
                            "@timestamp": {
                                "gte": "now-%sh/h"%since,
                                "lt": "now/d",
                                "format": "strict_date_time"
                            }
                        }
                    }
                },

                # "range": {
                #     "@timestamp": {
                #         "gte": "2015-01-01 00:00:00",
                #         "lte": "now",
                #         "format": "strict_date_time"
                #     }
                # }
            }
        }
        return base

    async def search(self, filter_find, filter_ignore,timelapse):
        # index_list = list(await self.indices.keys())
        # print(index_list)
        # last_index = sorted(index_list)[-1]

        try:
            query_body = self.query_builder(
                match_term=filter_find,
                ignore_term=filter_ignore,
                since=timelapse
            )
            count = await  self.es.count(index="*", body=query_body)
            result = await self.es.search(index="*", body=query_body, size=count["count"])
            # print(result)
            return result["hits"]["hits"]

        except Exception as e:
            logger.exception(e, exc_info=True)

    def close(self):
        """

        :return:
        """
        try:
            asyncio.ensure_future(self.es.close())
            logger.debug("Closed ES connection pool")
        except Exception as e:
            logger.error(e)

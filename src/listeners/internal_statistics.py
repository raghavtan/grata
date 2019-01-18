#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utilities import logger


class Statistics:
    """ Manage internal statistics """

    def __init__(self):
        self.alerts = dict(received=dict(api=0, queue=0), published=dict(api=0, queue=0))

    def update(self, state = None, hook=None):
        stats=self.alerts
        if state and hook:
            try:
                logger.debug("updating {} {}".format(state, hook))
                self.alerts[state][hook] = stats[state][hook] + 1
                logger.debug(self.alerts)
            except Exception as e:
                logger.exception("Catching Exception {}".format(e),exc_info=True)
        return stats


    def close(self):
        """

        :return:
        """
        pass

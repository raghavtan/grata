"""

"""
import json

import requests
from slackclient import SlackClient

from src.listeners import CreateSingleton
from utilities import logger


class ListenerClient(metaclass=CreateSingleton):
    """

    """
    def __init__(self, config):
        """

        :param config:
        """
        self.slacker = config.slack_url
        self.slacker_client = SlackClient(config.slack_token)

    def notification(self,
                     channel="ops-infra-alerts",
                     payload="sample"):
        """

        :param channel:
        :param payload:
        :return:
        """
        try:
            encoded_payload = json.dumps(payload, sort_keys=True, indent=4)
            headers = {'Content-type': 'application/json'}
            r = requests.post(self.slacker,
                              json={
                                  "text": "```%s```" % encoded_payload,
                                  "channel": "#%s" % channel,
                                  "username": "Notifier",
                                  "mrkdwn": "true"
                              },
                              headers=headers)

            out = {"text": r.text, "err": r.status_code, "sc": r.status_code}
            logger.debug(out)
        except Exception as e:
            out = str(e)
            logger.error(e)
        return out

    def close(self):
        """

        :return:
        """
        logger.info("Closing Slack connection pool")

    def channels(self):
        """

        :return:
        """
        channel_names = []
        channels = self.slacker_client.api_call("channels.list")
        for channel in channels["channels"]:
            channel_names.append(channel["name"])
        return channel_names

    def create_channel(self, name):
        """

        :param name:
        :return:
        """
        channel_create = self.slacker_client.api_call(
            "channels.create",
            name=name
        )
        logger.debug(channel_create)
        return channel_create

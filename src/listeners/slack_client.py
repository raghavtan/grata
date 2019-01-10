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
        self.default_channel = config.slack_default_channel

    def notification(self,
                     channel=None,
                     payload="sample",
                     slack_format=False):
        """

        :param channel:
        :param payload:
        :return:
        """
        try:
            if not channel:
                channel = self.default_channel
            logger.info("Sending Payload to slack")
            encoded_payload = json.dumps(payload, sort_keys=True, indent=4)
            headers = {'Content-type': 'application/json'}
            if not slack_format:
                r = requests.post(self.slacker,
                                  json={
                                      "text": "```%s```" % encoded_payload,
                                      "channel": "#%s" % channel,
                                      "username": "NotificationAlert",
                                      "mrkdwn": "true"
                                  },
                                  headers=headers)
            else:
                logger.debug("sending payload directly to slack")
                r = requests.post(self.slacker,
                                  json=encoded_payload,
                                  headers=headers)

            out = {"text": r.text, "sc": r.status_code}
            r.close()
            logger.debug(out)
        except Exception as e:
            out = str(e)
            logger.error(e)
        return out

    def close(self):
        """

        :return:
        """
        # logger.debug("Closed Slack connection pool")

    def channels(self):
        """

        :return:
        """
        return self.slacker_client.server.channels

    def create_channel(self, name):
        """

        :param name:
        :return:
        """

        out = dict(svc_channel=name)
        trace = "Create New Slack Channel [%s]" % name
        try:
            logger.debug(trace + " Initiated")
            channel_create = self.slacker_client.api_call(
                "channels.create",
                name=name
            )

            if channel_create["ok"] or (not channel_create["ok"] and channel_create["error"] == "name_taken"):
                if channel_create["ok"]:
                    self.notification(payload=trace)
                else:
                    logger.debug("Slack channel already exists [%s]" % name)
            else:
                out = "Error creating channel[%s:%s]" % (name,channel_create["error"])
                self.notification(payload=out)
            return out

        except Exception as e:
            logger.exception(e,exc_info=True)
            trace = "Error [%s] %s " % (e, trace)
            self.notification(payload=trace)
            return trace

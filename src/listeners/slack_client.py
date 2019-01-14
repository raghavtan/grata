"""

"""
import json

import requests
from slackclient import SlackClient

from src.listeners import CreateSingleton
from main import logger
from utilities.os_level import run_shell


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

            headers = {'Content-type': 'application/json'}
            if not slack_format:
                encoded_payload = json.dumps(payload, sort_keys=True, indent=4)
                r = requests.post(self.slacker,
                                  json={
                                      "text": "```%s```" % encoded_payload,
                                      "channel": "#%s" % channel,
                                      "username": "NotificationAlert",
                                      "mrkdwn": "true"
                                  },
                                  headers=headers)
                text = r.text
                rc = r.status_code
            else:
                payload["channel"] = channel
                encoded_payload = json.dumps(payload, sort_keys=True, indent=4)
                logger.debug("sending payload directly to slack")
                command = "curl -X POST --data-urlencode \'payload={PAYLOAD}\' {URL}"
                rc, output, text = run_shell(command=command.format(PAYLOAD=encoded_payload, URL=self.slacker))
                text="null"

            out = {"text": text, "sc": rc}
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
                out = "Error creating channel[%s:%s]" % (name, channel_create["error"])
                self.notification(payload=out)
            return out

        except Exception as e:
            logger.exception(e, exc_info=True)
            trace = "Error [%s] %s " % (e, trace)
            self.notification(payload=trace)
            return trace

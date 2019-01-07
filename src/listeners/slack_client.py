import json

import requests

from src.listeners import CreateSingleton
from utilities import logger
from slackclient import SlackClient


class ListenerClient(metaclass=CreateSingleton):
    def __init__(self, config):
        self.slacker = config.slack_url
        self.slacker_client = SlackClient(config.slack_token)

    async def notification(self, channel="ops-infra-alerts", payload="sample"):
        try:
            encoded_payload = json.dumps(payload)
            headers = {'Content-type': 'application/json'}
            r = requests.post(self.slacker, json={"text": "```%s```" % encoded_payload,
                                                  "channel": "#%s"%channel,
                                                  "username": "Notifier",
                                                  "mrkdwn": "true"
                                                  }, headers=headers)

            out = {"text": r.text, "err": r.status_code, "sc": r.status_code}
        except Exception as e:
            out = str(e)
        # out = self.slacker.api_call("chat.postMessage", channel=channel, text=payload)
        return out

    def close(self):
        logger.info("Closing Slack connection pool")

    async def channels(self):
        channel_names=[]
        channels = self.slacker_client.api_call("channels.list")
        for channel in channels["channels"]:
            channel_names.append(channel["name"])
        return channel_names

    def create_channel(self,name):
        channel_create = self.slacker_client.api_call("channels.create",name=name)
        return channel_create
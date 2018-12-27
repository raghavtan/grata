import json

import requests

from src.listeners import CreateSingleton
from utilities import logger


class ListenerClient(metaclass=CreateSingleton):
    def __init__(self, config):
        self.slacker = config.slack_url

    async def notification(self, channel="#ops-infra-alerts", payload="sample"):
        try:
            payload = {"text": "sample"}
            encoded_payload= json.dumps(payload)
            headers = {'Content-type': 'application/json'}
            r = requests.post(self.slacker, data=encoded_payload,headers=headers)
            out = {"text": r.text, "json": r.json(),"err":r.status_code,"sc":r.status_code}
        except Exception as e:
            out = str(e)
        # out = self.slacker.api_call("chat.postMessage", channel=channel, text=payload)
        return out

    def close(self):
        logger.info("Closing Slack connection pool")

    def channels(self):
        channels = self.slacker.api_call("channels.list")
        print(channels)

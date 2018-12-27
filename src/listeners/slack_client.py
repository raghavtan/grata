from slackclient import SlackClient

from src.listeners import CreateSingleton
from utilities import logger


class ListenerClient(metaclass=CreateSingleton):
    def __init__(self, config):
        self.slacker = SlackClient(config.slack_token)

    def notification(self, channel="#ops-infra-alerts", payload="sample"):
        print("sending notification to slack")
        out = self.slacker.api_call("chat.postMessage", channel=channel, text=payload)
        return out

    def close(self):
        logger.info("Closing Slack connection pool")

    def channels(self):
        channels = self.slacker.api_call("channels.list")
        print(channels)

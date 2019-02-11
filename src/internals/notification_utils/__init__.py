"""

"""
import json
import re
import time

from numba import jit

from utilities import logger

tsdb_amq_regex = r".*\.(?P<consumer>\S+-service(-hack)?)\.VirtualTopic\.[Ll][tT]\.(?P<producer>\S+)-service\S*"
amq_regex = re.compile(tsdb_amq_regex)

payload_dump = {
    "attachments": [
        {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "warning",
            "author_name": "LimeTray/Alerter",
            "title": "Please Fix ME",
            "text": "",
            "footer": "LimeTray Engineering API",
            "ts": int(time.time())

        }
    ],
    "channel": "sampler5",
    "username": "UnDefinedUser",
}


@jit(nopython=True)
def payload_multiplex(payload, source):
    color_dict = dict(OK="good", WARNING="warning", CRITICAL="danger")
    slack_payload = payload_dump
    slack_channel = "sampler5"
    slack_username = "UnDefinedUser"
    slack_color = "warning"
    text = payload
    slack_title = "Please Fix ME"
    slack_author = "LimeTray/Alerter"
    if source == "jenkins":
        slack_payload = payload
        slack_channel = payload["text"]
        slack_username = payload["text"]

    elif source == "tsdb":
        slack_author = "InfluxTSDB/QueryEngine"
        slack_color = color_dict[payload["level"]]
        try:
            if "VirtualTopic" in payload["id"]:
                queue = payload["data"]["series"][0]["tags"]["destinationName"]
                queue_name_parts = amq_regex.match(queue).groupdict()
                slack_channel = queue_name_parts["consumer"]
                slack_title = queue_name_parts["consumer"]
                value = payload["data"]["series"][0]["values"][0][-1]
                broker = payload["data"]["series"][0]["name"].replace("_Queues", "")
                text = "Queue: {QUEUE}\nBroker: {BROKER}\nValue: {VALUE}".format(QUEUE=queue, BROKER=broker,
                                                                                 VALUE=value)
                if "DLQ" in queue or "Dead" in queue:
                    slack_username = "DLQ/Dead Queue Threshold"
                else:
                    slack_username = "Consumer-Queue Slow Consumption"

            elif "compute.internal" in payload["id"]:
                slack_channel = "infrastructure"
                slack_title = "Kubernetes Node"
                slack_username = "System Resource Usage"
                value = payload["data"]["series"][0]["values"][0][-1]
                queue = payload["data"]["series"][0]["tags"]["nodename"]
                text = "Node: {QUEUE}\nDimension: {BROKER}\nThreshold: {VALUE}".format(QUEUE=queue,
                                                                                       BROKER=
                                                                                       payload["data"]["series"][0][
                                                                                           "name"].upper(),
                                                                                       VALUE=value)
        except Exception as e:
            logger.exception(e, exc_info=True)

    elif source == "sns":
        try:
            slack_channel = "infrastructure"
            slack_username = "AWS/SNS Notification"
            color_dict = dict(OK="good", ALARM="danger")
            message = json.loads(payload["Message"])
            queue = "%s::%s" % (message["Trigger"]["MetricName"], message["Trigger"]["Namespace"])
            broker = message["Trigger"]["Dimensions"][0]["value"]
            value = message["Trigger"]["Threshold"]
            slack_color = color_dict[message["NewStateValue"]]
            text = "MetricName: {QUEUE}\nDimension: {BROKER}\nThreshold: {VALUE}".format(QUEUE=queue, BROKER=broker,
                                                                                         VALUE=value)
            slack_title = message["AlarmName"]
            slack_author = "Amazon Web Services/SNS [CloudCompliance]"
        except Exception as e:
            logger.exception(e, exc_info=True)

    else:
        text = payload

    slack_payload["channel"] = slack_channel
    slack_payload["username"] = slack_username
    slack_payload["attachments"][0]["color"] = slack_color
    slack_payload["attachments"][0]["text"] = text
    slack_payload["attachments"][0]["title"] = slack_title
    slack_payload["attachments"][0]["title"] = slack_author
    logger.debug("Channel: %s\nNew Payload: %s" % (slack_channel, slack_payload))

    return slack_payload, {"name": slack_channel}

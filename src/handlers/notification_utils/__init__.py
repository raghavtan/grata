"""

"""
import json
import re
import time

from utilities import logger

tsdb_amq_regex = r".*\.(?P<consumer>\S+)-service\.VirtualTopic\.[Ll][tT]\.(?P<producer>\S+)-service\S*"
amq_regex = re.compile(tsdb_amq_regex)


def payload_multiplex(payload, source):
    color = dict(OK="good", WARNING="warning", CRITICAL="danger")
    payload_restructured = payload
    if source == "jenkins":
        name_service = payload["text"]
        payload_restructured["channel"] = name_service
        payload_restructured["username"] = name_service
    elif source == "tsdb":
        if "VirtualTopic" in payload["id"]:
            queue = payload["data"]["series"][0]["tags"]["destinationName"]
            queue_name_parts = amq_regex.match(queue).groupdict()
            name_service = "%s-service" % queue_name_parts["consumer"]
            channel = name_service
            value = payload["data"]["series"][0]["values"][0][-1]
            broker = payload["data"]["series"][0]["name"].replace("_Queues", "")
            text = "Queue: {QUEUE}\nBroker: {BROKER}\nValue: {VALUE}".format(QUEUE=queue, BROKER=broker, VALUE=value)
            if "DLQ" in queue or "Dead" in queue:
                alert_username = "DLQ/Dead Queue Threshold"
            else:
                alert_username = "Consumer-Queue Slow Consumption"
            tl_1_dashboard = "tl-dashboard.limetray.com:8161/admin/browse.jsp?JMSDestination="
            tl_2_dashboard = "tl-dashboard-2.limetray.com:8161/admin/browse.jsp?JMSDestination="
            if queue.endswith("1"):
                dashboard = tl_1_dashboard + queue
            else:
                dashboard = tl_2_dashboard + queue
        elif "compute.internal" in payload["id"]:
            channel = "infrastructure"
            name_service = "Kubernetes Node"
            alert_username = "System Resource Usage"
            value = payload["data"]["series"][0]["values"][0][-1]
            queue = payload["data"]["series"][0]["tags"]["nodename"]
            text = "Node: {QUEUE}\nDimension: {BROKER}\nThreshold: {VALUE}".format(QUEUE=queue,
                                                                                   BROKER=payload["data"]["series"][0][
                                                                                       "name"].upper(),
                                                                                   VALUE=value)
            dashboard=""
        payload_restructured = {
            "attachments": [
                {
                    "fallback": "Required plain-text summary of the attachment.",
                    "color": color[payload["level"]],
                    "author_name": "InfluxTSDB/QueryEngine",
                    "title": name_service,
                    "text": "%s\n%s" % (text, dashboard),
                    "footer": "LimeTray Engineering API",
                    "ts": int(time.time())

                }
            ],
            "channel": channel,
            "username": alert_username,
        }
    elif source == "sns":
        channel = "infrastructure"
        color = dict(OK="good", ALARM="danger")
        message = json.loads(payload_restructured["Message"])
        queue = "%s::%s" % (message["Trigger"]["MetricName"], message["Trigger"]["Namespace"])
        broker = message["Trigger"]["Dimensions"][0]["value"]
        value = message["Trigger"]["Threshold"]

        text = "MetricName: {QUEUE}\nDimension: {BROKER}\nThreshold: {VALUE}".format(QUEUE=queue, BROKER=broker,
                                                                                     VALUE=value)
        payload_restructured = {
            "attachments": [
                {
                    "fallback": "Required plain-text summary of the attachment.",
                    "color": color[message["NewStateValue"]],
                    "author_name": "Amazon Web Services/SNS [CloudCompliance]",
                    "title": message["AlarmName"],
                    "text": "%s" % text,
                    "footer": "LimeTray Engineering API",
                    "ts": int(time.time())

                }
            ],
            "channel": channel,
            "username": "AWS/SNS Notification",
        }
    else:
        channel = "sampler5"
    logger.debug("Channel: %s\nNew Payload: %s" % (channel, payload_restructured))

    return payload_restructured, {"name": channel}

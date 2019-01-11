"""

"""
import re

from utilities import logger

tsdb_amq_regex = r".*\.(?P<consumer>\S+)-service\.VirtualTopic\.[Ll][tT]\.(?P<producer>\S+)-service\S*"
amq_regex = re.compile(tsdb_amq_regex)


def payload_multiplex(payload, source):
    payload_restructured = payload
    if source == "jenkins":
        name_service = payload["text"]
        payload_restructured["channel"] = name_service
        payload_restructured["username"] = name_service
    elif source == "tsdb":
        color = dict(OK="good", WARNING="warning", CRITICAL="danger")
        queue = payload["data"]["series"][0]["tags"]["destinationName"]
        queue_name_parts = amq_regex.match(queue).groupdict()
        consumer = "%s-service" % queue_name_parts["consumer"]
        name_service = consumer
        value = payload["data"]["series"][0]["values"][0][-1]
        broker = payload["data"]["series"][0]["name"].replace("_Queues", "")
        text = "Queue: {QUEUE}\nBroker: {BROKER}\nValue: {VALUE}".format(QUEUE=queue, BROKER=broker, VALUE=value)
        if "DLQ" in queue or "Dead" in queue:
            alert_username = "DLQ/Dead Queue Threshold"
        else:
            alert_username = "Consumer-Queue Slow Consumption"
        tl_1_dashboard = "http://tl-dashboard.limetray.com:8161/admin/browse.jsp?JMSDestination="
        tl_2_dashboard = "http://tl-dashboard-2.limetray.com:8161/admin/browse.jsp?JMSDestination="
        if queue.endswith("1"):
            tl_dashboard = tl_1_dashboard + queue
        else:
            tl_dashboard = tl_2_dashboard + queue
        payload_restructured = {
            "attachments": [
                {
                    "fallback": "Required plain-text summary of the attachment.",
                    "color": color[payload["level"]],
                    "author_name": "InfluxTSDB/QueryEngine",
                    "title": name_service,
                    "text": text,

                }
            ],
            "channel": name_service,
            "username": alert_username,
            "url": tl_dashboard
        }
    else:
        name_service = "sampler5"
    logger.debug("Service: %s\nNew Payload: %s" % (name_service, payload_restructured))

    return payload_restructured, {"name": name_service}

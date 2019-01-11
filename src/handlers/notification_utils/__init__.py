"""

"""
from utilities import logger


def payload_multiplex(payload, source):
    payload_restructured = payload
    if source == "slack":
        name_service = payload["text"]
        payload_restructured["channel"] = name_service
        payload_restructured["username"] = name_service
    elif source == "tsdb":
        color = dict(OK="good", WARNING="warning", CRITICAL="danger")
        consumer = "%s-service" % payload["data"]["series"]["tags"]["consumer"]
        name_service = consumer
        queue = payload["data"]["series"]["tags"]["destinationName"]
        topic = payload["data"]["series"]["tags"]["topic"]
        value = payload["data"]["series"]["values"][0][1]
        broker = payload["data"]["series"]["broker"]
        text = "Queue: {QUEUE}\nBroker: {BROKER}\nTopic: {TOPIC}\nValue: {VALUE}".format(QUEUE=queue, BROKER=broker,
                                                                                         TOPIC=topic, VALUE=value)
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
            "username": name_service,
        }
    else:
        name_service ="sampler5"
    logger.info("::::::::::::::::::::::[ %s ]::::::::::::::::::::::" % name_service)

    return payload_restructured, {"name": name_service}
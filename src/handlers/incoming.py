"""

"""

from vibora.request import Request
from vibora.responses import JsonResponse

from src.handlers.notification_utils import service_name
from src.handlers.notification_utils.source_manager import source_manager
from src.listeners import CreateSingleton
from src.listeners.kafka_client import KafkaPublish
from src.listeners.slack_client import ListenerClient
from utilities import logger


def payload_restructure(payload, source):
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

    return payload_restructured,name_service


async def queue(request: Request):
    """

    :param request:
    :return:
    """
    try:
        logger.info("Received incoming alert")
        kaf = CreateSingleton.singleton_instances[KafkaPublish]
        payload = await request.json()
        resp = kaf.publish(payload)
        return JsonResponse({"status": "ok", "message": resp}, status_code=200)
    except Exception as e:
        resp = {"err": str.encode(str(e))}
        logger.error(resp)
        return JsonResponse(resp, status_code=400)


async def api(request: Request):
    """

    :param request:
    :return:
    """
    status = 400
    try:
        logger.info("Received incoming alert %s" % request.url)
        slc = CreateSingleton.singleton_instances[ListenerClient]

        payload = await request.json()
        logger.debug("Received alert payload\n%s" % payload)
        slack_direct_flag = False
        source = source_manager(payload)
        if source == "slack" or source == "tsdb":
            slack_direct_flag = True
            payload = payload_restructure(payload, source)
        resp = dict(service=None,
                    channel=None,
                    notification=None)
        svc = service_name(payload, slack_direct_flag)
        resp['service'] = svc
        if isinstance(resp["service"], dict):
            resp['channel'] = slc.create_channel(resp["service"]["name"])

        if isinstance(resp["channel"], dict):
            resp['notification'] = slc.notification(
                channel=resp["channel"]["svc_channel"],
                payload=payload,
                slack_format=slack_direct_flag
            )
        if isinstance(resp["notification"], dict):
            resp = {'message': resp["notification"]["text"]}
            status = 200
        logger.info("Sent payload to slack %s " % resp)
        return JsonResponse(resp, status_code=status)
    except Exception as e:
        resp = {"error": str.encode(str(e))}
        logger.error(resp)
        return JsonResponse(resp, status_code=status)

"""

"""

from vibora.request import Request
from vibora.responses import JsonResponse

from src.listeners import CreateSingleton
from src.listeners.kafka_client import KafkaPublish
from src.listeners.slack_client import ListenerClient
from utilities import logger


def service_name(payload,slack_payload_flag=False):
    """

    :param payload:
    :return:
    """
    if slack_payload_flag:
        name_service=payload["text"]
        logger.info("::::::::::::::::::::::[ %s ]::::::::::::::::::::::"%name_service)
    service = {"name": "sampler5"}
    return service


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
        if ["attachments", "channel", "username"] in payload.keys():
            slack_direct_flag = True
            del payload["channel"]
        resp = dict(service=None,
                    channel=None,
                    notification=None)
        svc = service_name(payload,slack_direct_flag)
        resp['service'] = svc
        if isinstance(resp["service"], dict):
            resp['channel'] = slc.create_channel(resp["service"]["name"])

        if isinstance(resp["channel"], dict):
            logger.debug(payload.keys())
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

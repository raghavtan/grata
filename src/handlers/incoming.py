"""

"""

from vibora.request import Request
from vibora.responses import JsonResponse

from src.handlers.notification_utils import payload_multiplex
from src.handlers.notification_utils.source_manager import source_manager
from src.listeners import CreateSingleton
from src.listeners.kafka_client import KafkaPublish
from src.listeners.slack_client import ListenerClient
from utilities import logger


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
        source, slack_direct_flag = source_manager(payload)
        payload_new, svc = payload_multiplex(payload, source)
        resp = dict(service=None,
                    channel=None,
                    notification=None)
        resp['service'] = svc
        if isinstance(resp["service"], dict):
            resp['channel'] = slc.create_channel(resp["service"]["name"])

        if isinstance(resp["channel"], dict):
            resp['notification'] = slc.notification(
                channel=resp["channel"]["svc_channel"],
                payload=payload_new,
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


# async def exec(request: Request):
#     """
#
#     :param request:
#     :return:
#     """
#     status = 400
#     try:
#         logger.info("Received incoming kuber alert trigger %s" % request.url)
#         slc = CreateSingleton.singleton_instances[ListenerClient]
#
#         payload = await request.json()
#         logger.debug("Received alert payload\n%s" % payload)
#         level=payload["level"]
#         node_name=payload["series"][0]["tags"]["nodename"]
#
#         logger.info("Sent payload to slack %s " % resp)
#         return JsonResponse(resp, status_code=status)
#     except Exception as e:
#         resp = {"error": str.encode(str(e))}
#         logger.error(resp)
#         return JsonResponse(resp, status_code=status)

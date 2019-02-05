"""

"""

import aiojobs
from vibora.request import Request
from vibora.responses import JsonResponse

from src.handlers.notification_utils import payload_multiplex
from src.handlers.notification_utils.source_manager import source_manager
from src.listeners import CreateSingleton
from src.listeners.kafka_client2 import KafkaPublish
from src.listeners.slack_client import ListenerClient
from utilities import logger


async def alert_job(request, slc, payload):
    try:
        source, slack_direct_flag = source_manager(payload)
        payload_new, svc = payload_multiplex(payload, source)
        resp = dict(service=svc,
                    channel=None,
                    notification=None)
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
            request.app.statistics.update("published", "api")
        logger.info("Sent payload to slack %s " % resp)
    except Exception as e:
        logger.exception(e,exc_info=True)


async def queue(request: Request):
    """

    :param request:
    :return:
    """
    try:

        logger.info(
            f'Received incoming alert '
            f'{request.client_ip} '
            f'{request.url} '
            f'{request.headers} '
            f'{request.method} '
            f'{request.protocol}')
        request.app.statistics.update("received", "queue")
        kaf = CreateSingleton.singleton_instances[KafkaPublish]
        payload = await request.json()
        resp = await kaf.publish(payload)
        request.app.statistics.update("published", "queue")
        return JsonResponse({"status": "ok", "message": resp._state}, status_code=200)
    except Exception as e:
        request.app.statistics.update("published", "queue")
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
        logger.info(
            f'Received incoming alert '
            f'{request.client_ip} '
            f'{request.url} '
            f'{request.headers} '
            f'{request.method} '
            f'{request.protocol}'
        )
        request.app.statistics.update("received", "api")
        slc = CreateSingleton.singleton_instances[ListenerClient]
        payload = await request.json()
        logger.debug("Received alert payload\n%s" % payload)
        scheduler = await aiojobs.create_scheduler(close_timeout=15)
        await scheduler.spawn(alert_job(request, slc, payload))
        resp = "ok"
        status = 200
    except Exception as e:
        resp = {"error": str.encode(str(e))}
        logger.exception(resp, exc_info=True)
    return JsonResponse({'msg': resp}, status_code=status)


async def exec(request: Request):
    """

    :param request:
    :return:
    """
    status = 400
    try:
        logger.info("Received incoming kuber alert trigger %s" % request.url)
        slc = CreateSingleton.singleton_instances[ListenerClient]

        payload = await request.json()
        logger.debug("Received alert payload\n%s" % payload)
        level = payload["level"]
        node_name = payload["series"][0]["tags"]["nodename"]

        logger.info("Sent payload to slack %s " % resp)
        return JsonResponse(resp, status_code=status)
    except Exception as e:
        resp = {"error": str.encode(str(e))}
        logger.error(resp)
        return JsonResponse(resp, status_code=status)

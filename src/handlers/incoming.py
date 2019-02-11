"""

"""

from vibora.request import Request
from vibora.responses import JsonResponse

from src.jobs.alert_job import Alerter
from src.listeners import CreateSingleton
from src.listeners.kafka_client2 import KafkaPublish
from src.listeners.slack_client import ListenerClient
from utilities import logger


async def queue(request: Request):
    """

    :param request:
    :return:
    """
    try:
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
        AlertJob = Alerter()
        request.app.statistics.update("received", "api")
        slc = CreateSingleton.singleton_instances[ListenerClient]
        payload = await request.json()
        logger.debug("Received alert payload\n%s" % payload)
        await request.app.scheduler.spawn(AlertJob.job(request, slc, payload))
        resp, status = "ok", 200
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
        logger.info("Received incoming kube alert trigger %s" % request.url)
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

"""

"""
from vibora.request import Request
from vibora.responses import JsonResponse

from src.listeners import CreateSingleton
from src.listeners.kafka_client import KafkaPublish
from utilities import logger


async def home(request: Request):
    """

    :param request:
    :param source:
    :return:
    """
    try:
        logger.info("Received incoming alert")
        kaf = CreateSingleton.singleton_instances[KafkaPublish]
        payload = await request.json()
        logger.debug("Request Arguments %s"%request.args)
        logger.debug("Request payload [%s]"%payload)
        resp = kaf.publish(payload=payload)
        return JsonResponse({"msg": resp}, status_code=200)
    except Exception as e:
        resp = {"err": str.encode(str(e))}
        logger.error(resp)
        return JsonResponse(resp, status_code=400)

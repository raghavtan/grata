"""

"""
from vibora.request import Request
from vibora.responses import JsonResponse
from vibora.responses import Response

from src.listeners import CreateSingleton
from src.listeners.slack_client import ListenerClient
from utilities import logger


async def service_name(slack_client, channel_list, payload):
    """

    :param slack_client:
    :param channel_list:
    :param payload:
    :return:
    """
    try:
        service = "devops"
        out = dict(svc_channel=service)
        trace = "Create new channel [%s]" % service
        if service not in channel_list:
            logger.info(trace + " Initiated")
            validate_get_svc = slack_client.create_channel(name=service)
            if not validate_get_svc["ok"]:
                out = "Error creating channel[%s]" % validate_get_svc["error"]
                trace = out
            slack_client.notification(channel="devops", payload=trace)
    except Exception as e:
        out = "Error [%s]" % e
    return out


async def home(request: Request, source: str):
    """

    :param request:
    :param source:
    :return:
    """
    if source:
        try:
            logger.info("Sending Payload to slack")
            slc = CreateSingleton.singleton_instances[ListenerClient]
            payload = await request.json()
            channel_list = slc.channels()
            svc = await service_name(slc, channel_list, payload)
            if isinstance(svc, dict):
                out = slc.notification(channel=svc["svc_channel"], payload=payload)
            else:
                out = svc
            if isinstance(out, dict):
                resp = {'msg': out["text"]}
                status = 200
            else:
                resp = {'err': out}
                status = 400
            logger.info("Sent payload to slack %s " % resp)
            return JsonResponse(resp, status_code=status)
        except Exception as e:
            resp = {"err": str.encode(str(e))}
            logger.info(resp)
            status = 400
            return JsonResponse(resp, status_code=status)

    else:
        try:
            return JsonResponse({'msg': "yo"})
        except Exception as e:
            return Response(str.encode(str(e)), status_code=200)

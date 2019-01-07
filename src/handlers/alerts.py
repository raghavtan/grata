"""

"""
from vibora.request import Request
from vibora.responses import JsonResponse
from vibora.responses import Response
import asyncio

from src.listeners import CreateSingleton
from src.listeners.slack_client import ListenerClient


def service_name(slack_client, channel_list, payload):
    try:
        service = "sampler2"
        out = dict(svc_channel=service)
        if service not in channel_list:
            print("Creating new channel [%s]" % service)
            validate_get_svc = slack_client.create_channel(name=service)
            if not validate_get_svc["ok"]:
                out = "Error creating channel[%s]" % validate_get_svc["error"]
    except Exception as e:
        out = "Error [%s]" % e
    return out


async def home(request: Request, source: str):
    loop = asyncio.get_event_loop()
    if source:
        try:
            print("Sending Payload to slack")
            slc = CreateSingleton.singleton_instances[ListenerClient]
            payload = await request.json()
            channel_list = slc.channels()
            svc = service_name(slc, channel_list, payload)
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
            print("Sent payload to slack %s "%resp)
            return JsonResponse(resp, status_code=status)
        except Exception as e:
            resp = {"err": str.encode(str(e))}
            print(resp)
            status = 400
            return JsonResponse(resp, status_code=status)

    else:
        try:
            return JsonResponse({'msg': "yo"})
        except Exception as e:
            return Response(str.encode(str(e)), status_code=200)

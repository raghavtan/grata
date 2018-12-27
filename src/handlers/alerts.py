"""

"""
from vibora.request import Request
from vibora.responses import JsonResponse
from vibora.responses import Response

from src.listeners import CreateSingleton
from src.listeners.slack_client import ListenerClient


async def home(request: Request, source: str):
    if source:
        try:
            slc = CreateSingleton.singleton_instances[ListenerClient]
            out = await slc.notification()
            # slc.channels()
            print("+=====================+\n%s\n::::::::"%out)
            if isinstance(out, dict):
                print("if if no fail")
                payload = await request.json()
                print(payload)
                resp = {'msg': "ok"}
                status = 200
                return JsonResponse(resp, status_code=status)
            else:
                print("notif")
                resp = {'err': out}
                status = 400
                return JsonResponse(resp, status_code=status)
        except Exception as e:
            resp = {"err": str.encode(str(e))}
            status = 400
            return JsonResponse(resp, status_code=status)

    else:
        try:
            return JsonResponse({'msg': "yo"})
        except:
            print("lllllllllllll")
            return Response(str.encode(str(e)), status_code=200)

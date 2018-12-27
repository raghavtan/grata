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
            slc.notification()
            # slc.channels()
            payload = request.json()
            print(payload)
            return JsonResponse({'msg': str(payload)})
        except Exception as e:
            return Response(str.encode(str(e)), status_code=301)

    else:
        try:
            return JsonResponse({'msg': "yo"})
        except:
            print("lllllllllllll")
            return Response(str.encode(str(e)), status_code=200)

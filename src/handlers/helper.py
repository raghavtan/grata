"""

"""
from vibora.request import Request
from vibora.responses import JsonResponse


async def home(request: Request, source: dict):
    if source:
        return JsonResponse({'msg': source})
    else:
        return JsonResponse({'msg': "invalid api help [could not find prefix apis]"})

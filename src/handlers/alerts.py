"""

"""
from vibora.request import Request
from vibora.responses import JsonResponse


async def home(request: Request,source: str):
    if source:
        return JsonResponse({'msg': source})
    else:
        return JsonResponse({'msg': "yo"})

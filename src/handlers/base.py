"""

"""
from vibora.request import Request
from vibora.responses import JsonResponse


async def base(request: Request):
    return JsonResponse({'msg': "base"})


async def health(request: Request):
    return JsonResponse({'msg': "health"})


async def stats(request: Request):
    return JsonResponse({'msg': "stats"})

async def routes(request: Request):
    return JsonResponse({'msg': "stats"})

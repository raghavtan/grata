"""

"""
from vibora.request import Request
from vibora.responses import JsonResponse



async def base(request: Request):
    """

    :param request:
    :return:
    """
    return JsonResponse({'msg': "base"})


async def health(request: Request):
    """

    :param request:
    :return:
    """
    return JsonResponse({'msg': "health"})


async def stats(request: Request):
    """

    :param request:
    :return:
    """
    return JsonResponse({'msg': "stats"})


async def routes(request: Request):
    """

    :param request:
    :return:
    """
    return JsonResponse({'msg': "stats"})

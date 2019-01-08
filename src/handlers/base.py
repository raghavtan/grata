"""

"""
from vibora.request import Request
from vibora.responses import JsonResponse

from src.listeners import CreateSingleton
from src.listeners.slack_client import ListenerClient


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
    try:
        slc = CreateSingleton.singleton_instances[ListenerClient]
        slc.notification()
    except Exception as e:
        print(e)
        raise
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

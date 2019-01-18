"""

"""
from vibora.request import Request
from vibora.responses import JsonResponse
from utilities import logger


async def base(request: Request):
    """

    :param request:
    :return:
    """
    logger.info(
        f'Received incoming alert '
        f'{request.client_ip} '
        f'{request.url} '
        f'{request.headers} '
        f'{request.method} '
        f'{request.protocol}')
    return JsonResponse({'msg': "base"})


async def health(request: Request):
    """

    :param request:
    :return:
    """
    logger.info(
        f'Received incoming alert '
        f'{request.client_ip} '
        f'{request.url} '
        f'{request.headers} '
        f'{request.method} '
        f'{request.protocol}')
    return JsonResponse({'msg': "health"})


async def stats(request: Request):
    """

    :param request:
    :return:
    """

    logger.info(
        f'Received incoming alert '
        f'{request.client_ip} '
        f'{request.url} '
        f'{request.headers} '
        f'{request.method} '
        f'{request.protocol}')
    return JsonResponse({'msg': request.app.statistics.update()})


async def routes(request: Request):
    """

    :param request:
    :return:
    """
    logger.info(
        f'Received incoming alert '
        f'{request.client_ip} '
        f'{request.url} '
        f'{request.headers} '
        f'{request.method} '
        f'{request.protocol}')
    return JsonResponse({'msg': "stats"})

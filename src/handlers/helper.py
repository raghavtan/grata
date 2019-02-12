"""

"""
from vibora.request import Request
from vibora.responses import JsonResponse

from utilities import logger


async def home(request: Request, source: dict):
    """

    :param request:
    :param source:
    :return:
    """
    logger.info(
        f'Received incoming alert '
        f'{request.client_ip} '
        f'{request.url} '
        f'{request.headers} '
        f'{request.method} '
        f'{request.protocol}')
    if source:
        return JsonResponse({'msg': source})
    else:
        return JsonResponse({'msg': "invalid api help [could not find prefix apis]"})

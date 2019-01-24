"""

"""
from vibora.request import Request
from vibora.responses import JsonResponse

from src.resources.rds.rds import parsed_events
from src.resources.reports import report_generate
from utilities import logger


async def generate(request: Request):
    """

    :param request:
    :return:
    """
    status = 400
    try:
        format = {
            "title": "title",
            "payload": "json for report",
            "bucket": "bucket",
            "lapse": "timelapse"
        }
        logger.info(
            f'Received incoming alert '
            f'{request.client_ip} '
            f'{request.url} '
            f'{request.headers} '
            f'{request.method} '
            f'{request.protocol}')
        payload = await request.json()
        if format.keys() in payload.keys():
            report_url = report_generate(list_of_print=payload["payload"],
                                         timelapse=payload["lapse"],
                                         title=payload["title"],
                                         bucket=payload["bucket"])
            resp = report_url
            status = 200
        else:
            resp = "Bad Format of POST request :::: %s"%format.keys()
    except Exception as e:
        resp = e
        logger.exception(e, exc_info=True)
    return JsonResponse({'msg': resp}, status_code=status)


async def parse(request: Request):
    """

    :param request:
    :return:
    """
    status = 400
    try:
        format = {
            "rdsinstance": "rdsinstance",
            "timelapse": "timelapse",
        }
        logger.info(
            f'Received incoming alert '
            f'{request.client_ip} '
            f'{request.url} '
            f'{request.headers} '
            f'{request.method} '
            f'{request.protocol}')
        payload = await request.json()
        if format.keys() in payload.keys():
            report_url = parsed_events(dBInstanceIdentifier=payload["rdsinstance"],
                                       days_to_ingest=payload["timelapse"],
                                       )
            resp = report_url
            status = 200
        else:
            resp = "Bad Format of POST request :::: %s"%format.keys()
    except Exception as e:
        resp = e
        logger.exception(e, exc_info=True)
    return JsonResponse({'msg': resp}, status_code=status)


async def health(request: Request):
    """

    :param request:
    :return:
    """
    return JsonResponse({'msg': "health"})

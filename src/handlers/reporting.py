"""

"""
import aiojobs
from vibora.request import Request
from vibora.responses import JsonResponse

from src.resources.ansible_mail import send_mail
from src.resources.rds.rds import parsed_events
from src.resources.reports import report_generate
from utilities import logger
import time


async def report_job(resource, time_lapse):
    all_rds = parsed_events(days_to_ingest=int(time_lapse / 24))
    logger.info("Fetched Parsed logs for all_rds")
    for instance, events in all_rds.items():
        url = report_generate(events,
                              timelapse=24,
                              title="%s-%s" % (resource, instance))
        logger.info("Generated xlsx file at %s" % url)
        send_mail(subject="%s Query Report" % instance, body=url,toaddr="tech@limetray.com")
        logger.info("Sent Mail")


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
        if set(format.keys()) == set(payload.keys()):
            report_url = report_generate(list_of_print=payload["payload"],
                                         timelapse=payload["lapse"],
                                         title=payload["title"],
                                         bucket=payload["bucket"])
            resp = report_url
            status = 200
        else:
            resp = "Bad Format of POST request :::: %s" % format
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
        if set(format.keys()) in set(payload.keys()):
            report_url = parsed_events(dBInstanceIdentifier=payload["rdsinstance"],
                                       days_to_ingest=payload["timelapse"],
                                       )
            resp = report_url
            status = 200
        else:
            resp = "Bad Format of POST request :::: %s" % format
    except Exception as e:
        resp = e
        logger.exception(e, exc_info=True)
    return JsonResponse({'msg': resp}, status_code=status)


async def complete(request: Request, resource: str, time_lapse: int):
    """

    :param request:
    :return:
    """
    status = 400
    try:

        logger.info(
            f'Received incoming alert '
            f'{request.client_ip} '
            f'{request.url} '
            f'{request.headers} '
            f'{request.method} '
            f'{request.protocol}')
        if resource:
            resp = []
            status = 200
            if resource == "rds":
                scheduler = await aiojobs.create_scheduler(close_timeout=15)
                await scheduler.spawn(report_job(resource, time_lapse))
                resp = "ok"
            else:
                resp = "Only RDS reports configured"
        else:
            resp = "Specify Resource for report"
    except Exception as e:
        resp = e
        logger.exception(e, exc_info=True)
    return JsonResponse({'msg': resp}, status_code=status)


async def complete_without_time(request: Request, resource: str):
    """

    :param request:
    :return:
    """
    status = 400
    try:
        time_lapse = 24
        logger.info(
            f'Received incoming alert '
            f'{request.client_ip} '
            f'{request.url} '
            f'{request.headers} '
            f'{request.method} '
            f'{request.protocol}')
        if resource:
            print(resource)
            print(time_lapse)
            resp = resource
        else:
            resp = "Specify Resource for report"
    except Exception as e:
        resp = e
        logger.exception(e, exc_info=True)
    return JsonResponse({'msg': resp}, status_code=status)

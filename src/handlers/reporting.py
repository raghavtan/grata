"""

"""
from vibora.request import Request
from vibora.responses import JsonResponse

from src.jobs.reporting_job import Report
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
    :param resource:
    :param time_lapse:
    :return:
    """
    status = 400
    try:
        ReportJob = Report()
        if resource:
            status = 200
            if resource == "rds":
                await request.app.scheduler.spawn(ReportJob.job(resource, time_lapse))
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
    :param resource:
    :return:
    """
    status = 400
    try:
        time_lapse = 24
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

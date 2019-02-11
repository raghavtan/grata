from src.resources.ansible_mail import send_mail
from src.resources.rds.rds import parsed_events, fetch_all_rds
from src.resources.reports import report_generate
from utilities import logger


class Report:

    async def job(self, resource, time_lapse):
        rds_names = fetch_all_rds()
        for instance in rds_names:
            events = parsed_events(dBInstanceIdentifier=instance,
                                   days_to_ingest=int(time_lapse / 24))
            logger.info("Fetched Parsed logs for %s" % instance)
            if len(events) > 0:
                url = report_generate(events,
                                      timelapse=24,
                                      title="%s-%s" % (resource, instance))
                logger.info("Generated xlsx file at %s" % url)
                send_mail(subject="%s Query Report" % instance, body=url,
                          toaddr="tech@limetray.com")
                logger.info("Sent Mail for %s" % instance)

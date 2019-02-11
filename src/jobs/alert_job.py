from src.internals.notification_utils import payload_multiplex
from src.internals.notification_utils.source_manager import sources
from utilities import logger


class Alerter:

    async def job(self, request, slc, payload):
        try:
            source, slack_direct_flag = sources(payload)
            payload_new, svc = payload_multiplex(payload, source)
            resp = dict(service=svc,
                        channel=None,
                        notification=None)
            if isinstance(resp["service"], dict):
                resp['channel'] = slc.create_channel(resp["service"]["name"])

            if isinstance(resp["channel"], dict):
                resp['notification'] = slc.notification(
                    channel=resp["channel"]["svc_channel"],
                    payload=payload_new,
                    slack_format=slack_direct_flag
                )
            if isinstance(resp["notification"], dict):
                resp = {'message': resp["notification"]["text"]}
                request.app.statistics.update("published", "api")
            logger.info("Sent payload to slack %s " % resp)
        except Exception as e:
            logger.exception(e, exc_info=True)

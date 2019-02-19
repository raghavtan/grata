from src.listeners import CreateSingleton
from src.listeners.elastic import EsClient
from src.resources.ansible_mail import send_mail
from src.resources.rds.rds import parsed_events, fetch_all_rds
from src.resources.reports import report_generate
from utilities import logger


class Report:

    async def job_rds(self, resource, time_lapse):
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
                          toaddr="tech@limetray.com",resource="RDS")
                logger.info("Sent Mail for %s" % instance)

    async def job_redis(self, time_lapse):
        es_client = CreateSingleton.singleton_instances[EsClient]
        result = await es_client.search(filter_find=[{
            "input_type": "redis"
        }],
            filter_ignore=[
                {
                    "message": "info"
                },
                {
                    "fields_redis_node": "test_redis"
                }
            ],
            timelapse=time_lapse
        )
        logger.info("Fetched Parsed logs for Redis Nodes")
        parsed_events_list = []
        if len(result) > 0:
            for event in result:
                parsed_event = {
                    "Query_Time":
                        event["_source"]["redis_slowlog_duration_us"]
                        if "redis_slowlog_duration_us" in event["_source"].keys()
                        else "",
                    "Command":
                        event["_source"]["redis_slowlog_cmd"]
                        if "redis_slowlog_cmd" in event["_source"].keys()
                        else "",
                    "Command_Arguments":
                        event["_source"]["redis_slowlog_args"]
                        if "redis_slowlog_args" in event["_source"].keys()
                        else "",
                    "Redis_Node":
                        event["_source"]["source"]
                        if "source" in event["_source"].keys()
                        else "",
                    "Timestamp":
                        event["_source"]["@timestamp"]
                        if "@timestamp" in event["_source"].keys()
                        else "",
                }
                parsed_events_list.append(parsed_event)

            url = report_generate(parsed_events_list,
                                  timelapse=time_lapse,
                                  title="Redis")
            logger.info("Generated xlsx file at %s" % url)
            send_mail(subject="Redis Query Report", body=url, resource="REDIS",
                      toaddr="tech@limetray.com")
            logger.info("Sent Mail for %s" % url)

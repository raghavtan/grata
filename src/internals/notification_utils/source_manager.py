"""

"""

from utilities import logger


class AlertsSource:
    """

    """
    jenkins = ["attachments", "channel"]
    bugsnag = ["account", "project"]
    logs = ["check_result", "stream"]
    service = ["microservice"]
    tsdb = ["data", "message", "duration", "level", "previousLevel"]
    sns = ["UnsubscribeURL", "TopicArn"]
    third_party = []

    @classmethod
    def __key_set__(cls):
        """

        :return:
        """
        return_list = []
        sources_list = list(AlertsSource.__dict__.keys())
        for source in sources_list:
            if not source.startswith("__"):
                return_list.append(source)

        return return_list


def sources(payload=None):
    """

    :param payload:
    :return:
    """
    slack_direct_sources = ["jenkins", "tsdb", "bugsnag", "sns"]
    slack_direct_flag = False
    sources_list = AlertsSource.__key_set__()
    payload_keys = set(list(payload.keys()))
    for source_name in sources_list:
        sub_check = set(AlertsSource.__dict__[source_name])
        if sub_check.issubset(payload_keys):
            if source_name in slack_direct_sources:
                slack_direct_flag = True
            logger.debug("Source: %s |AND| Flag: %s" % (source_name, slack_direct_flag))
            return source_name, slack_direct_flag

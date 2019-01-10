"""

"""


class AlertsSource:
    """

    """
    slack = ["attachments", "channel"]
    bugnsag = ["account", "project"]
    logs = ["check_result", "stream"]
    service = ["microservice"]
    tsdb = ["data","message","duration","level","previousLevel"]
    third_party = []

    @classmethod
    def __key_set__(cls):
        """

        :return:
        """
        sources = []
        sources_list = list(AlertsSource.__dict__.keys())
        for source in sources_list:
            if not source.startswith("__"):
                sources.append(source)

        return sources


def source_manager(payload=None):
    """

    :param payload:
    :return:
    """
    sources_list = AlertsSource.__key_set__()
    payload_keys = set(list(payload.keys()))
    for source_name in sources_list:
        sub_check = set(AlertsSource.__dict__[source_name])
        if sub_check.issubset(payload_keys):
            return source_name

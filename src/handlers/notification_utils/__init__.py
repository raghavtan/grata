"""

"""
from utilities import logger


def service_name(payload, slack_payload_flag=False):
    """

    :param payload:
    :return:
    """
    if slack_payload_flag:
        name_service = payload["text"]
        logger.info("::::::::::::::::::::::[ %s ]::::::::::::::::::::::" % name_service)
    service = {"name": "sampler5"}
    return service

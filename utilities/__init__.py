import logging
import sys

import json_logging

json_logging.ENABLE_JSON_LOGGING = True
json_logging.init()
logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Config:
    """

    """
    def __init__(self, config: dict):
        """

        :param config:
        """
        for key, value in config.items():
            setattr(self, key, value)


async def __routes_list_filter__(app, url_filter="/"):
    """

    :param app:
    :param url_filter:
    :return:
    """
    map_routes = {}
    for patterns in app.routes:
        decoded_pattern = patterns.simplified_pattern.decode("utf-8")
        handler_str = str("%s::%s" % (sys.modules[patterns.handler.__module__].__name__,
                                      patterns.handler.__name__))
        if (decoded_pattern.startswith(url_filter) and
                decoded_pattern != url_filter and
                decoded_pattern != url_filter + "/" and not
                handler_str.startswith("src.server") and
                decoded_pattern.endswith("/")):
            unpack_method_list = []
            for unpack_methods in list(patterns.methods):
                unpack_method_list.append(unpack_methods.decode("utf-8"))

            map_routes[decoded_pattern] = dict(methods=unpack_method_list,
                                               params=patterns.params_book,
                                               handler=handler_str.replace("src.handlers.", ""))
    return map_routes

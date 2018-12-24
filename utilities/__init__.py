import json_logging
import logging
import sys


class Config:
    def __init__(self, config: dict):
        for key, value in config.items():
            setattr(self, key, value)


json_logging.ENABLE_JSON_LOGGING = True
json_logging.init()
logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

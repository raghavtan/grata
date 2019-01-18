import json_logging
import logging
from src.listeners import CreateSingleton
from src.listeners.log_factory import LogFactory

json_logging.ENABLE_JSON_LOGGING = True
json_logging.COMPONENT_NAME="Grata"
json_logging.init()
logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
kh = CreateSingleton.singleton_instances[LogFactory]
logger.addHandler(kh)
logger.info("TCP Logger Initialized")
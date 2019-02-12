"""

"""
import json
import os

from src.server import Server
from utilities import Config
from utilities import logger
from utilities.termination_protection import TerminateProtected

BASE_PATH = os.path.abspath(os.getcwd())


def main():
    """

    :return:
    """
    with TerminateProtected():
        try:
            with open('config.json') as f:
                config = Config(json.load(f))
                config.home_path = BASE_PATH
                server = Server(config)
                server.load_routes()
                server.start()
                server.stop()
        except Exception as e:
            logger.exception("Shutting Down[Crash] %s" % e)


if __name__ == '__main__':
    main()

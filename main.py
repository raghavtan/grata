"""

"""
import json

from src.server import Server
from utilities import Config
from utilities.termination_protection import TerminateProtected
from utilities import logger


def main():
    """

    :return:
    """
    with TerminateProtected():
        try:
            with open('config.json') as f:
                config = Config(json.load(f))
                server = Server(config)
                server.load_routes()
                server.start()
                server.stop()
        except Exception as e:
            logger.exception("Shutting Down[Crash] %s" % e)


if __name__ == '__main__':
    main()

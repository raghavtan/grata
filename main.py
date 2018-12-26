import json

from src.server import Server
from utilities import Config


def main():
    with open('config.json') as f:
        config = Config(json.load(f))
        server = Server(config)
        server.load_routes()
        server.start()


if __name__ == '__main__':
    main()

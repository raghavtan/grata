"""

"""
import asyncio

import aiojobs
from vibora import Request
from vibora import Response
from vibora import Vibora
from vibora.hooks import Hook, Events
from vibora.responses import JsonResponse
from vibora.router import RouterStrategy
from vibora.router.router import Route

from src.listeners import CreateSingleton
from src.listeners.internal_statistics import Statistics
from src.listeners.kafka_client2 import KafkaPublish
from src.listeners.slack_client import ListenerClient
from src.routes_loader import ServerRoutes
from utilities import __routes_list_filter__
from utilities import logger


class Server(object):
    """

    """

    def __init__(self, config):
        """

        :param config:
        """

        self.app = Vibora(router_strategy=RouterStrategy.CLONE, log=self.log_handler)
        self.config = config
        self.app.statistics = Statistics()
        self.app.components.add(self.config)
        self.config_parser_restructure()
        if self.config.api_helper.upper() == "True".upper():
            self.load_inbuilt_routes()
        self.startup_handling()
        self.closure_handling()
        self.event_handling()

    def config_parser_restructure(self):
        if self.config.strict_slashes.upper() == "True".upper():
            self.config.slashes = True
        else:
            self.config.slashes = False
        if self.config.alert_queue.upper() == "True".upper():
            self.config.enable_queue = True
        else:
            self.config.enable_queue = False

    def load_inbuilt_routes(self):
        """

        :return:
        """
        logger.info("Loading inbuilt routes")
        self.app.add_route(Route(pattern=str.encode("/routes"), handler=self.url_map))

    def load_routes(self):
        """

        :return:
        """
        logger.info("Loading routes from config")
        apis_base = ServerRoutes(self)
        apis_base.traverse_route_tree()

    def closure_handling(self):
        """

        :return:
        """
        closure_hook = Hook(
            Events.BEFORE_SERVER_STOP,
            handler=CreateSingleton.__clean_all__
        )
        self.app.add_hook(closure_hook)

    async def startup_init(self):
        logger.info("Initializing Slack connection")
        ListenerClient(self.config)
        if self.config.enable_queue:
            logger.info("Initializing Kafka connection")
        KafkaPublish(self.config, asyncio.get_event_loop())
        self.app.scheduler = await aiojobs.create_scheduler(close_timeout=30)

        # self.init_socket_server()
        # if self.config.kafka_logging.upper() == "True".upper():
        #     LogFactory(self.config,asyncio.get_event_loop())
        #     from utilities.log_factory import logger as kafka_logger
        #     kafka_logger.info("Kafka Logger Initialized")

    def startup_handling(self):
        """

        :return:
        """
        startup_hook = Hook(
            Events.AFTER_SERVER_START,
            handler=self.startup_init
        )
        self.app.add_hook(startup_hook)

    def event_handling(self):
        """

        :return:
        """
        request_hook = Hook(
            Events.AFTER_ENDPOINT,
            handler=self.request_logger
        )
        # response_hook = Hook(
        #     Events.AFTER_RESPONSE_SENT,
        #     handler=self.response_logger
        # )
        self.app.add_hook(request_hook)
        # self.app.add_hook(response_hook)

    def request_logger(self, request: Request):
        logger.info(
            f'Received Incoming\n'
            f'{request.url}\n'
            f'{request.headers.__str__()}\n'
            f'{request.method}')

    def response_logger(self, response: Response):

        logger.info(
            f'Request Response\n'
            f'{dir(response)}\n')

    async def url_filter_map(self, request: Request):
        """

        :param request:
        :return:
        """
        filter = request.url.decode("utf-8")
        url_json = await __routes_list_filter__(self.app, url_filter=filter)
        return JsonResponse(url_json, status_code=404)

    async def url_map(self, request: Request):
        """

        :param request:
        :return:
        """
        # logger.info(
        #     f'Received incoming alert '
        #     f'{request.client_ip} '
        #     f'{request.url} '
        #     f'{request.headers} '
        #     f'{request.method} '
        #     f'{request.protocol}')
        url_json = await __routes_list_filter__(self.app)
        return JsonResponse(url_json)

    @staticmethod
    def log_handler(msg, level):
        """

        :param msg:
        :param level:
        :return:
        """
        # Redirecting the msg and level to logging library.
        getattr(logger, level)(msg)
        print(f'Msg: {msg} / Level: {level}')

    def start(self):
        """

        :return:
        """
        logger.info("Starting Server %s" % self.config.name)
        self.app.run(host=self.config.host,
                     port=self.config.port,
                     )

    def stop(self):
        """

        :return:
        """
        logger.info("Stopping server")
        self.app.clean_up()

    def application(self):
        """

        :return:
        """
        return self.app

    def init_socket_server(self):
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(handle_echo, '0.0.0.0', 8282, loop=loop)
        loop.create_task(coro)
        asyncio.ensure_future(coro)


async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))

    print("Send: %r" % message)
    writer.write(data)
    await writer.drain()

    print("Close the client socket")
    writer.close()

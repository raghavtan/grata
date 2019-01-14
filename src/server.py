"""

"""
from vibora import Request
from vibora import Vibora
from vibora.hooks import Hook, Events
from vibora.responses import JsonResponse
from vibora.router import RouterStrategy
from vibora.router.router import Route

from src.listeners import CreateSingleton
from src.listeners.slack_client import ListenerClient
from src.listeners.kafka_client import KafkaPublish
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
        self.app = Vibora(router_strategy=RouterStrategy.CLONE, log=logger)
        self.config = config
        self.app.components.add(self.config)
        self.config_parser_restructure()
        if self.config.api_helper.upper() == "True".upper():
            self.load_inbuilt_routes()
        logger.info("Initializing Slack connection")
        ListenerClient(config)
        if self.config.enable_queue:
            logger.info("Initializing Kafka connection")
        KafkaPublish(config)
        self.closure_handling()

    def config_parser_restructure(self):
        if self.config.strict_slashes.upper() == "True".upper():
            self.config.slashes = True
        else:
            self.config.slashes = False
        if self.config.alert_queue.upper() == "True".upper():
            self.config.enable_queue=True
        else:
            self.config.enable_queue=False


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

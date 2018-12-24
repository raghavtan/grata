"""

"""
from vibora import Request
from vibora import Vibora
from vibora.responses import JsonResponse
from vibora.router import RouterStrategy
from vibora.router.router import Route

from src.routes_loader import ServerRoutes
from utilities import logger
from utilities import __routes_list_filter__


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
        if config.api_helper.upper() == "True".upper():
            self.load_inbuilt_routes()

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

    def load_inbuilt_routes(self):
        """

        :return:
        """
        self.app.add_route(Route(pattern=str.encode("/routes"), handler=self.url_map))

    def load_routes(self):
        """

        :return:
        """
        apis_base = ServerRoutes(self)
        apis_base.traverse_route_tree()

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
                     debug=bool(self.config.debug),
                     )

    def application(self):
        return self.app

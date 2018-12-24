import sys

from vibora import Request
from vibora import Vibora
from vibora.responses import JsonResponse
from vibora.router import RouterStrategy
from vibora.router.router import Route

from src.routes_loader import ServerRoutes
from utilities import logger


class Server(object):

    def __init__(self, config):
        self.app = Vibora(router_strategy=RouterStrategy.CLONE, log=logger)
        self.config = config
        self.app.components.add(self.config)
        self.load_inbuilt_routes()

    def load_inbuilt_routes(self):
        self.app.add_route(Route(pattern=str.encode("/routes"), handler=self.url_map))

    async def url_filter_map(self, request: Request):
        filter = request.url.decode("utf-8")
        url_json = await __routes_list_filter__(self.app, url_filter=filter)
        return JsonResponse(url_json)

    async def url_map(self, request: Request):
        url_json = await __routes_list_filter__(self.app)
        return JsonResponse(url_json)

    def load_routes(self):
        apis_base = ServerRoutes(self)
        apis_base.traverse_route_tree()

    @staticmethod
    def log_handler(msg, level):
        # Redirecting the msg and level to logging library.
        getattr(logger, level)(msg)
        print(f'Msg: {msg} / Level: {level}')

    def start(self):
        logger.info("Starting Server %s" % self.config.name)
        self.app.run(host=self.config.host,
                     port=self.config.port,
                     debug=bool(self.config.debug),
                     )

    def application(self):
        return self.app


async def __routes_list_filter__(app, url_filter="/"):
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

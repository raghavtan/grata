"""

"""
import os

from vibora.router.router import Route

from src.cache_engine import DefaultCacheEngine
from src.routes import RouteData
from src.routes.routes import routes as app_routes


def helper_route(server, app, prefix, route):
    base_path=prefix
    if prefix.endswith(">"):
        base_path = os.path.dirname(prefix)
        special_route = RouteData(handler=route.handler, methods=None,cache=True)
    else:
        special_route = RouteData(handler=server.url_filter_map, methods=None)
    create_route(route_parent=app, route=special_route, path=base_path)


def create_route(route_parent, route, path, strict_slashes=False):
    """

    :param route_parent:
    :param route:
    :param path:
    :return:
    """
    route_list = []
    methods_list = []
    path = path.replace("//", "/")
    if route.cache:
        cache_engine = DefaultCacheEngine(skip_hooks=True)
    else:
        cache_engine = None
    for route_method in route.methods:
        methods_list.append(route_method.upper())
    route_remodeled_slash_free = Route(
        pattern=str.encode(path),
        handler=route.handler,
        methods=methods_list,
        cache=cache_engine
    )
    route_list.append(route_remodeled_slash_free)
    if len(path) > 1 and not path.endswith("/"):
        route_remodeled_slash_inclusive = Route(
            pattern=str.encode(path + "/"),
            handler=route.handler,
            methods=methods_list,
            cache=cache_engine
        )
        route_list.append(route_remodeled_slash_inclusive)
    for internal_route_object in route_list:
        route_parent.add_route(internal_route_object)


class ServerRoutes:
    """

    """

    def __init__(self, server):
        """

        :param server:
        """
        self.server = server
        self.application = server.application()
        self.route_tree = app_routes

    def traverse_route_tree(self, parent=None, tree=None, path="/"):
        if not parent:
            parent = self.application
        if not tree:
            tree = self.route_tree
        for tree_path, tree_value in tree.items():
            if isinstance(tree_value, dict):
                self.traverse_route_tree(
                    tree=tree_value, path=path + tree_path
                )
                if self.server.config.api_helper.upper() == "True".upper():
                    helper_route(self.server, parent, path + tree_path, tree_value)
            elif isinstance(tree_value, RouteData):
                create_route(parent, tree_value, path + tree_path)
                if self.server.config.api_helper.upper() == "True".upper():
                    helper_route(self.server, parent, path + tree_path, tree_value)
            else:
                raise ValueError('Expecting dict or route data type in route tree')

    def __validateRouteHandler__(self, handler):
        pass

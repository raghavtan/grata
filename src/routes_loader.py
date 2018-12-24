"""

"""
import os

from vibora.router.router import Route

from src.cache_engine import DefaultCacheEngine
from src.routes import RouteData
from src.routes.routes import routes as app_routes


def helper_route(server, app, prefix, route):
    if prefix.endswith(">"):
        base_path = os.path.dirname(prefix)
        create_route(route_parent=app, route=route, path=base_path)
    else:
        special_route = RouteData(handler=server.url_filter_map)
        create_route(route_parent=app, route=special_route, path=prefix)


def create_route(route_parent, route, path):
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

        :param application:
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
                helper_route(self.server, parent, path + tree_path, tree_value)
            elif isinstance(tree_value, RouteData):
                helper_route(self.server, parent, path + tree_path, tree_value)
                create_route(parent, tree_value, path + tree_path)
            else:
                raise ValueError('Expecting dict or route data type in route tree')


    def __validateRouteHandler__(self, handler):
        pass

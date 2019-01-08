"""

"""
import os

from vibora.router.router import Route

from src.cache_engine import DefaultCacheEngine
from src.routes import RouteData
from src.routes.routes import routes as app_routes


def _route_internal_(route, methods_list, cache_engine, path, strict_slashes=False):
    """

    :param route:
    :param methods_list:
    :param cache_engine:
    :param path:
    :param strict_slashes:
    :return:
    """
    route_list = []
    path_list_base = [path]
    path_list = []
    path_last_suffix = os.path.basename(os.path.normpath(path))
    path_prefix = os.path.dirname(path)

    if path_last_suffix.startswith("<") and path_last_suffix.endswith(">"):
        path_list_base.append(path_prefix)

    for path_element in path_list_base:
        if not strict_slashes and len(path_element) > 2:
            path_list.append(path_element.rstrip("/"))
            path_list.append(str(path_element + "/"))
        else:
            path_list.append(path_element)
    for route_element in list(set(path_list)):
        route_remodeled = Route(
            pattern=str.encode(route_element),
            handler=route.handler,
            methods=methods_list,
            cache=cache_engine
        )
        route_list.append(route_remodeled)

    return route_list


def create_route(route_parent, route, path, strict_slashes=False):
    """

    :param route_parent:
    :param route:
    :param path:
    :param strict_slashes:
    :return:
    """
    methods_list = []
    path = path.replace("//", "/")
    if route.cache:
        cache_engine = DefaultCacheEngine(skip_hooks=True)
    else:
        cache_engine = None
    for route_method in route.methods:
        methods_list.append(route_method.upper())
    route_list = _route_internal_(route, methods_list, cache_engine, path, strict_slashes)
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
        """

        :param parent:
        :param tree:
        :param path:
        :return:
        """
        if not parent:
            parent = self.application
        if not tree:
            tree = self.route_tree
        for tree_path, tree_value in tree.items():
            if isinstance(tree_value, dict):
                self.traverse_route_tree(
                    tree=tree_value, path=path + tree_path
                )
            elif isinstance(tree_value, RouteData):

                create_route(parent, tree_value, path + tree_path, self.server.config.slashes)
            else:
                raise ValueError('Expecting dict or route data type in route tree')

    def __validateRouteHandler__(self, handler):
        pass

from src.handlers import alerts
from src.handlers import base
from src.handlers import incoming
from src.routes import RouteData
from src.handlers import reporting

routes = {
    "/": RouteData(cache=True,
                   methods=None,
                   handler=base.base,
                   parameters=""),
    "/health": RouteData(cache=True,
                         handler=base.health),
    # "/stats": RouteData(cache=None,
    #                     handler=base.stats),
    "/alerts": {
        "/v1": {
            "/<source>": RouteData(cache=True,
                                   methods=['GET', 'POST'],
                                   handler=alerts.home)
        }
    },
    "/incoming": {
        "/api": RouteData(cache=None,
                          methods=['GET', 'POST'],
                          handler=incoming.api),

        "/queue": RouteData(cache=None,
                            methods=['GET', 'POST'],
                            handler=incoming.queue),

        "/exec": RouteData(cache=None,
                           methods=['GET', 'POST'],
                           handler=incoming.api)
    },
    "/report": {
        "/parse": RouteData(cache=None,
                          methods=[ 'POST'],
                          handler=reporting.parse),

        "/generate": RouteData(cache=None,
                            methods=[ 'POST'],
                            handler=reporting.generate),

    }
}

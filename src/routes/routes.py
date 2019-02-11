from src.handlers import alerts
from src.handlers import base
from src.handlers import incoming
from src.handlers import reporting
from src.routes import RouteData

routes = {
    "/": RouteData(cache=True,
                   methods=None,
                   handler=base.base,
                   parameters=""),
    "/health": RouteData(cache=None,
                         handler=base.health),
    "/alerts": {
        "/v1": {
            "/<source>": RouteData(cache=True,
                                   methods=['GET', 'POST'],
                                   handler=alerts.home)
        }
    },
    "/incoming": {
        "/api": RouteData(cache=None,
                          methods=[ 'POST'],
                          handler=incoming.api),

        "/queue": RouteData(cache=None,
                            methods=['POST'],
                            handler=incoming.queue),

        "/exec": RouteData(cache=None,
                           methods=['GET', 'POST'],
                           handler=incoming.api)
    },
    "/report": {
        "/<resource>/<time_lapse>": RouteData(cache=None,
                                              methods=['GET'],
                                              handler=reporting.complete),
        "/<resource>/": RouteData(cache=None,
                                  methods=['GET'],
                                  handler=reporting.complete_without_time),
        "/parse": RouteData(cache=None,
                            methods=['POST'],
                            handler=reporting.parse),

        "/generate": RouteData(cache=None,
                               methods=['POST'],
                               handler=reporting.generate),

    }
}

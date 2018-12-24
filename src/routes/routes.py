from src.handlers import alerts
from src.handlers import base
from src.routes import RouteData

routes = {
    "/": RouteData(cache=True,
                   methods=None,
                   handler=base.base,
                   parameters=""),
    "/health": RouteData(cache=True,
                         handler=base.health),
    "/_stats": RouteData(cache=True,
                         handler=base.stats),
    "/alerts": {
        "/v1": {
            "/<source>": RouteData(cache=True,
                                   methods=['GET', 'POST'],
                                   handler=alerts.home)
        }
    }
}

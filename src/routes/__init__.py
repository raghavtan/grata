class RouteData:
    def __init__(self, handler, cache=None, methods=None, parameters=""):
        self.cache = cache
        if not methods:
            self.methods = ['GET']
        else:
            self.methods = methods
        self.handler = handler
        self.parameters = parameters

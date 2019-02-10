import logging

class RouteFilter():
    """
    Filter based on request route

    Methods:
        ignore
    """
    def __init__(self, routes = None, logger=None):
        """
        Initialize filter

        Arguments:
            routes: list of routes to be filtered. If empty, no route will be filtereed
            logger: logger instance of python's standard logging library
        """
        self.routes = routes or []
        self.logger = logger or logging.getLogger(__name__)
    
    def ignore(self, request):
        """
        Checks if requested route should be ignored 

        Arguments:            
            request: flask app request context
        """
        self.logger.debug("ignore called")

        route = request.url_rule.endpoint

        self.logger.debug("checking route: {route}".format(route=route))

        should_ignore = route in self.routes
        
        self.logger.debug("ignore finished with result: {should_ignore}".format(should_ignore=should_ignore))
        return should_ignore
import logging

class RouteUidProvider():
    """
    UID provider for requester's IP+route.

    Methods:
        get_uid
    """
    def __init__(self,ip_uid_provider, logger=None):
        """
        Initialize provider

        Arguments:
            ip_uid_provider = instance of IpUidProvider
            logger: logger instance of python's standard logging library
        """
        self.ip_uid_provider = ip_uid_provider
        self.logger = logger or logging.getLogger(__name__)
    
    def get_uid(self, request):
        """
        Returns the requester's IP + the requested route as a uid.

        Arguments:            
            request: flask app request context
        """
        self.logger.debug("get_uid called")

        ip = self.ip_uid_provider.get_uid(request)
        
        route = request.url_rule.endpoint

        uid = "{ip}_{route}".format(ip=ip, route=route)
        
        self.logger.debug("get_uid finished with result: {uid}".format(uid=uid))
        return uid
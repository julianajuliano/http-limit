import logging

class IpUidProvider():
    """
    UID provider for requester's IP.

    Methods:
        get_uid
    """
    def __init__(self, ip_resolver, logger=None):
        """
        Initialize provider

        Arguments:
            ip_resolver: instance of IpResolver
            logger: logger instance of python's standard logging library
        """
        self.ip_resolver = ip_resolver
        self.logger = logger or logging.getLogger(__name__)
    
    def get_uid(self, request):
        """
        Returns the requester's IP as a uid.

        Arguments:            
            request: flask app request context
        """
        self.logger.debug("get_uid called")

        ip = self.ip_resolver.get_ip(request)
        
        self.logger.debug("get_uid finished with result: {ip}".format(ip=ip))
        return ip
import logging

class IpFilter():
    """
    Filter based on requester IP

    Methods:
        ignore
    """
    def __init__(self, ip_resolver, ips = None, logger=None):
        """
        Initialize filter

        Arguments:
            ips: list of IPs to be filtered. If empty, no IP will be filtereed
            logger: logger instance of python's standard logging library
        """
        self.ip_resolver = ip_resolver
        self.ips = ips or []
        self.logger = logger or logging.getLogger(__name__)
    
    def ignore(self, request):
        """
        Checks if requester IP should be ignored 

        Arguments:            
            request: flask app request context
        """
        self.logger.debug("ignore called")

        ip = self.ip_resolver.get_ip(request)

        should_ignore = ip in self.ips
        
        self.logger.debug("ignore finished with result: {should_ignore}".format(should_ignore=should_ignore))
        return should_ignore
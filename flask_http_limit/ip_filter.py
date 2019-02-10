import logging

class IpFilter():
    """
    Filter based on requester IP

    Methods:
        ignore
    """
    def __init__(self, ips = None, logger=None):
        """
        Initialize filter

        Arguments:
            ips: list of IPs to be filtered. If empty, no IP will be filtereed
            logger: logger instance of python's standard logging library
        """
        self.ips = ips or []
        self.logger = logger or logging.getLogger(__name__)
    
    def ignore(self, request):
        """
        Checks if requester IP should be ignored 

        Arguments:            
            request: flask app request context
        """
        self.logger.debug("ignore called")

        x_fowarded = request.headers.getlist("X-Forwarded-For")
        self.logger.debug("X-Forwarded-For: {x_fowarded}".format(x_fowarded=x_fowarded))

        self.logger.debug("remote_addr: {remote_addr}".format(remote_addr=request.remote_addr))

        if x_fowarded:
         ip = x_fowarded[0]
        else:
            ip = request.remote_addr

        should_ignore = ip in self.ips
        
        self.logger.debug("ignore finished with result: {should_ignore}".format(should_ignore=should_ignore))
        return should_ignore
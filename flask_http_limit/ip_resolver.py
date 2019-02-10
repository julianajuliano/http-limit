import logging

class IpResolver():
    """
    Resolves requester's IP.

    Methods:
        get_ip
    """
    def __init__(self,logger=None):
        """
        Initialize resolver

        Arguments:            
            logger: logger instance of python's standard logging library
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def get_ip(self, request):
        """
        Returns the requester's IP.

        Arguments:            
            request: flask app request context
        """
        self.logger.debug("get_ip called")

        x_fowarded = request.headers.getlist("X-Forwarded-For")
        self.logger.debug("X-Forwarded-For: {x_fowarded}".format(x_fowarded=x_fowarded))

        self.logger.debug("remote_addr: {remote_addr}".format(remote_addr=request.remote_addr))

        if x_fowarded:
         ip = x_fowarded[0]
        else:
            ip = request.remote_addr
        
        self.logger.debug("get_ip finished with result: {ip}".format(ip=ip))
        return ip
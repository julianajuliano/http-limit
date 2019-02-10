import logging
from redis import ConnectionError
from http import HTTPStatus

from . import HttpLimitError

#http status for this rule
LIMIT_ERROR_MESSAGE = "Rate limit exceeded. Try again in {ttl} seconds."
CONNECTION_ERROR_MESSAGE = "Error calculating rate limit."

class LimitByTimeRule():
    """
    Limiting rule based on requests x time. Uses redis as data storage.

    Methods:
        apply
    """
    def __init__(self, redis_client, time_limit, request_limit, fail_on_connection_error=True, logger=None):
        """
        Initialize rule.

        Arguments:
            redis_client: redis client instance
            time_limit: time limit in seconds 
            request_limit: maximum requests per time_limit
            fail_on_connection_error: indicates weather a failed connection with redis should raise an exception
            logger: logger instance of python's standard logging library
        """
        self.redis_client = redis_client
        self.time_limit = time_limit
        self.request_limit = request_limit
        self.fail_on_connection_error = fail_on_connection_error
        self.logger = logger or logging.getLogger(__name__)

    def apply(self, uid):
        """
        Apply limiting rule based on uid.
        """
        self.logger.debug("[{uid}] apply called".format(uid=uid))
        try:
            current_value = self.redis_client.get(uid)
            self.logger.debug("[{uid}] current count: {current_value}".format(uid=uid,current_value=current_value))
            
            if not current_value:
                self.redis_client.set(uid, 1, ex=self.time_limit)

                self.logger.debug("[{uid}] count set to 1.".format(uid=uid))

                self.logger.debug("apply finished")
                return
            
            count = int(current_value)
            if count >= self.request_limit:
                ttl = self.redis_client.ttl(uid)
                self.logger.debug("[{uid}] limit reached, ttl: {ttl}".format(uid=uid,ttl=ttl))

                raise HttpLimitError(HTTPStatus.TOO_MANY_REQUESTS, LIMIT_ERROR_MESSAGE.format(ttl=ttl))
            
            self.redis_client.incr(uid)
            self.logger.debug("[{uid}] count incremented by 1.".format(uid=uid))
            self.logger.debug("apply finished")
            
        except ConnectionError:
            if self.fail_on_connection_error:
                self.logger.error("[{uid}] error connecting to redis.".format(uid=uid), exc_info=True)
                raise HttpLimitError(HTTPStatus.INTERNAL_SERVER_ERROR, CONNECTION_ERROR_MESSAGE.format(ttl=5))
            
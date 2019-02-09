from . import HttpLimitError
from redis import ConnectionError
from http import HTTPStatus

#http status for this rule
LIMIT_ERROR_MESSAGE = "Rate limit exceeded. Try again in {ttl} seconds."
CONNECTION_ERROR_MESSAGE = "Error calculating rate limit."

class LimitByTimeRule():
    def __init__(self, redis_client, time_limit, request_limit, fail_on_connection_error=True):
        self.redis_client = redis_client
        self.time_limit = time_limit
        self.request_limit = request_limit
        self.fail_on_connection_error = fail_on_connection_error

    def apply(self, uid):
        try:
            current_value = self.redis_client.get(uid)
            
            if not current_value:
                self.redis_client.set(uid, 1, ex=self.time_limit)
                return
            
            count = int(current_value)
            if count >= self.request_limit:
                ttl = self.redis_client.ttl(uid)
                raise HttpLimitError(HTTPStatus.TOO_MANY_REQUESTS, LIMIT_ERROR_MESSAGE.format(ttl=ttl))
            
            self.redis_client.incr(uid)
        except ConnectionError:
            if self.fail_on_connection_error:
                raise HttpLimitError(HTTPStatus.INTERNAL_SERVER_ERROR, CONNECTION_ERROR_MESSAGE.format(ttl=5))
            
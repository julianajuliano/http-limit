
class LimitByTimeRule():
    def __init__(self, redis_client, time_limit, request_limit):
        self.redis_client = redis_client
        self.time_limit = time_limit
        self.request_limit = request_limit

    def can_execute(self, uid):
        current_value = self.redis_client.get(uid)
        
        if not current_value:
            self.redis_client.set(uid, 1, ex=self.time_limit)
            return True
        
        count = int(current_value)
        if count >= self.request_limit:
            return False
        
        self.redis_client.incr(uid)

        return True

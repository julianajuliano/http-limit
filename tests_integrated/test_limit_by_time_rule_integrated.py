import pytest
import re
import time
from grappa import should
from http import HTTPStatus
from redis import StrictRedis

from flask_http_limit import LimitByTimeRule, HttpLimitError

class TestLimitByTimeRuleIntegrated():
    def setup_method(self):
        self.unavailable_redis_client = StrictRedis(host='localhost', port=666, db=0, decode_responses=True)
        self.redis_client = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
        self.redis_client.flushdb()
    
    def test_should_raise_HttpLimitError_when_execution_count_exceeded(self):
        time_limit = 10
        limit_by_time = LimitByTimeRule(self.redis_client, time_limit, 3)
        uid = "test1"

        limit_by_time.apply(uid)
        limit_by_time.apply(uid)
        limit_by_time.apply(uid)
        #sleep for 1 second
        time.sleep(1) 
        
        #limit reached
        with pytest.raises(HttpLimitError) as exinfo:
            limit_by_time.apply(uid)
        
        exception = exinfo.value
        exception.status_code | should.be.equal.to(HTTPStatus.TOO_MANY_REQUESTS)
        
        match = re.findall("\d+", exception.message)
        match | should.have.length.of(1)
        ttl_integer = int(match[0])
        ttl_integer | should.be.equal.to(time_limit - 1)
        
    def test_should_run_when_execution_count_not_exceeded(self):
        limit_by_time = LimitByTimeRule(self.redis_client, 10, 4)
        uid = "test2"

        limit_by_time.apply(uid)
        limit_by_time.apply(uid)
        limit_by_time.apply(uid)
        limit_by_time.apply(uid)

    def test_should_raise_HttpLimitError_when_redis_is_not_available(self):
        limit_by_time = LimitByTimeRule(self.unavailable_redis_client, 10, 4, fail_on_connection_error=True)
        uid = "test4"

        with pytest.raises(HttpLimitError) as exinfo:
            limit_by_time.apply(uid)

        exception = exinfo.value
        exception.status_code | should.be.equal.to(HTTPStatus.INTERNAL_SERVER_ERROR)
        exception.message | should.match("Error calculating rate limit.")

    def test_should_run_when_configured_to_run_and_redis_is_not_available(self):        
        limit_by_time = LimitByTimeRule(self.unavailable_redis_client, 10, 4, fail_on_connection_error=False)
        uid = "test3"

        limit_by_time.apply(uid)

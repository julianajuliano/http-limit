import pytest
from grappa import should
from http import HTTPStatus

from mocks import MockRedisClient
from flask_http_limit import LimitByTimeRule, HttpLimitError
import flask_http_limit.http_limit



class TestLimitByTimeRule():
    
    def test_should_raise_HttpLimitError_when_execution_count_exceeded(self):
        redis_client_mock = MockRedisClient()
        time_limit = 10
        request_limit = 3
        limit_by_time = LimitByTimeRule(redis_client_mock, time_limit, request_limit)
        uid = "unittest1"

        for i in range(0, request_limit):
            limit_by_time.apply(uid)
                
        #limit reached
        with pytest.raises(HttpLimitError) as exinfo:
            limit_by_time.apply(uid)
        
        exception = exinfo.value
        exception.status_code | should.be.equal.to(HTTPStatus.TOO_MANY_REQUESTS)
        exception.message | should.match("Rate limit exceeded. Try again in \d+ seconds.")

    
    def test_should_run_when_execution_count_not_exceeded(self):
        redis_client_mock = MockRedisClient()
        time_limit = 10
        request_limit = 4
        limit_by_time = LimitByTimeRule(redis_client_mock, time_limit, request_limit)
        uid = "unittest2"

        for i in range(0,request_limit):
            limit_by_time.apply(uid)

        
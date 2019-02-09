from grappa import should

from mocks import MockRedisClient
from flask_http_limit import LimitByTimeRule

class TestLimitByTimeRule():
    
    def test_should_return_false_when_execution_count_exceeded(self):
        redis_client_mock = MockRedisClient()
        limit_by_time = LimitByTimeRule(redis_client_mock, 10, 3)
        uid = "unittest1"

        limit_by_time.can_execute(uid) | should.be.true        
        limit_by_time.can_execute(uid) | should.be.true        
        limit_by_time.can_execute(uid) | should.be.true        
        
        #limit reached
        limit_by_time.can_execute(uid) | should.be.false        
    
    def test_should_return_true_when_execution_count_not_exceeded(self):
        redis_client_mock = MockRedisClient()
        limit_by_time = LimitByTimeRule(redis_client_mock, 10, 4)
        uid = "unittest2"

        limit_by_time.can_execute(uid) | should.be.true        
        limit_by_time.can_execute(uid) | should.be.true        
        limit_by_time.can_execute(uid) | should.be.true        
        limit_by_time.can_execute(uid) | should.be.true
        
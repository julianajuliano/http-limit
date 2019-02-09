from grappa import should
from redis import StrictRedis

from flask_http_limit import LimitByTimeRule

class TestLimitByTimeRuleIntegrated():
    def setup_method(self):
        self.redis_client = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
        self.redis_client.flushdb()
    
    def test_should_return_false_when_execution_count_exceeded(self):
        limit_by_time = LimitByTimeRule(self.redis_client, 10, 3)
        uid = "test1"

        limit_by_time.can_execute(uid) | should.be.true        
        limit_by_time.can_execute(uid) | should.be.true        
        limit_by_time.can_execute(uid) | should.be.true        
        
        #limit reached
        limit_by_time.can_execute(uid) | should.be.false
        
    
    def test_should_return_true_when_execution_count_not_exceeded(self):
        limit_by_time = LimitByTimeRule(self.redis_client, 10, 4)
        uid = "test2"

        limit_by_time.can_execute(uid) | should.be.true
        limit_by_time.can_execute(uid) | should.be.true
        limit_by_time.can_execute(uid) | should.be.true
        limit_by_time.can_execute(uid) | should.be.true
        
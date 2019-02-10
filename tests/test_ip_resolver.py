"""
Unit tests for IpResolver
"""

from grappa import should
from flask_http_limit import IpResolver
from mocks import MockRequest

class TestIpResolver():
    def setup_method(self):
        self.ip_resolver = IpResolver()
    
    def test_should_return_ip(self):
        ip = "127.0.0.1"
        request_mock = MockRequest(ip)
        
        result = self.ip_resolver.get_ip(request_mock)

        result | should.be.equal.to(ip)
        
    def test_should_return_first_ip_fowarded(self):
        ip = "127.0.0.1"
        x_fowarded = ["127.0.0.2", "127.0.0.3", "127.0.0.4"]
        request_mock = MockRequest(ip, x_fowarded)
        
        result = self.ip_resolver.get_ip(request_mock)

        result | should.be.equal.to(x_fowarded[0])
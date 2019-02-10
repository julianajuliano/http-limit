"""
Unit tests for IpFilter
"""

from grappa import should
from flask_http_limit import IpFilter
from mocks import MockRequest

class TestIpUidProvider():
        
    def test_should_return_false_when_filter_is_empty(self):
        ip = "127.0.0.1"
        request_mock = MockRequest(ip)
        ip_filter = IpFilter()
        
        result = ip_filter.ignore(request_mock)

        result | should.be.false
    
    def test_should_return_false_when_filter_does_not_contain_ip(self):
        ip = "127.0.0.1"
        request_mock = MockRequest(ip)
        ip_filter = IpFilter(["127.0.0.2"])
        
        result = ip_filter.ignore(request_mock)

        result | should.be.false

    def test_should_return_true_when_filter_contains_ip(self):
        ip = "127.0.0.1"
        request_mock = MockRequest(ip)
        ip_filter = IpFilter(["127.0.0.2", ip])
        
        result = ip_filter.ignore(request_mock)

        result | should.be.true
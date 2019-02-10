"""
Unit tests for IpUidProvider
"""

from grappa import should
from flask_http_limit import IpUidProvider
from mocks import MockIpResolver, MockRequest

class TestIpUidProvider():
    def test_should_return_ip(self):
        ip = "127.0.0.1"
        request_mock = MockRequest(ip)
        ip_resolver_mock = MockIpResolver(ip)
        ip_uid_provider = IpUidProvider(ip_resolver_mock)
        
        result = ip_uid_provider.get_uid(request_mock)

        result | should.be.equal.to(ip)
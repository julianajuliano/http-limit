"""
Unit tests for RouteUidProvider
"""

from grappa import should
from flask_http_limit import RouteUidProvider
from mocks import MockRequest, MockIpResolver

class TestRouteUidProvider():
    
    def test_should_return_ip_plus_route(self):
        ip = "127.0.0.1"
        route = "test1"
        request_mock = MockRequest(ip, route=route)
        route_uid_provider = RouteUidProvider(MockIpResolver(ip=ip))
        
        result = route_uid_provider.get_uid(request_mock)

        result | should.be.equal.to("{ip}_{route}".format(ip=ip, route=route))       
    
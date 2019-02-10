"""
Unit tests for RouteUidProvider
"""

from grappa import should
from flask_http_limit import RouteUidProvider
from mocks import MockRequest, MockUidProvider

class TestRouteUidProvider():
    
    def test_should_return_ip_plus_route_when_(self):
        ip = "127.0.0.1"
        route = "test1"
        request_mock = MockRequest(ip, route=route)
        route_uid_provider = RouteUidProvider(MockUidProvider(uid=ip))
        
        result = route_uid_provider.get_uid(request_mock)

        result | should.be.equal.to("{ip}_{route}".format(ip=ip, route=route))
        
    def test_should_return_first_ip_fowarded_plus_route(self):
        ip = "127.0.0.1"
        x_fowarded = ["127.0.0.2", "127.0.0.3", "127.0.0.4"]
        route = "test2"
        request_mock = MockRequest(ip, x_fowarded,route=route)
        route_uid_provider = RouteUidProvider(MockUidProvider(uid=x_fowarded[0]))
        
        result = route_uid_provider.get_uid(request_mock)

        result | should.be.equal.to("{ip}_{route}".format(ip=x_fowarded[0], route=route))
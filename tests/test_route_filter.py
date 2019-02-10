"""
Unit tests for RouteFilter
"""

from grappa import should
from flask_http_limit import RouteFilter
from mocks import MockRequest

class TestIpUidProvider():
        
    def test_should_return_false_when_filter_is_empty(self):
        route = "test1"
        request_mock = MockRequest(route=route)
        route_filter = RouteFilter()
        
        result = route_filter.ignore(request_mock)

        result | should.be.false
    
    def test_should_return_false_when_filter_does_not_contain_route(self):
        route = "test2"
        request_mock = MockRequest(route=route)
        route_filter = RouteFilter(["testx"])
        
        result = route_filter.ignore(request_mock)

        result | should.be.false

    def test_should_return_true_when_filter_contains_route(self):
        route = "test3"
        request_mock = MockRequest(route=route)
        route_filter = RouteFilter(["testx", route])
        
        result = route_filter.ignore(request_mock)

        result | should.be.true
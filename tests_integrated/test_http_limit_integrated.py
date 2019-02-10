"""
Integration tests for HttpLimit extension. 

Runs a flask app on a local server with the HttpLimit extesion plugged.

Requires:
A running redis instance on localhost por 6379.
"""
import pytest
import logging
import requests
import time
import sys
from flask_testing import LiveServerTestCase
from flask import Flask
from grappa import should
from http import HTTPStatus
from redis import StrictRedis

from flask_http_limit import HttpLimit, LimitByTimeRule, IpUidProvider, IpFilter, RouteFilter

class BaseHttpLimitIntegratedTest(LiveServerTestCase):

    def init_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 5000
        app.config['LIVESERVER_TIMEOUT'] = 10

        app.add_url_rule("/", "index", view_func=self._view)
        app.add_url_rule("/test", "test", view_func=self._view)

        return app

    def init_http_limit(self):
        """
        To be overwritten by child classes
        """
        pass

    def create_app(self):
        
        app = self.init_app()

        self.redis_client = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
        self.redis_client.flushdb()

        self.time_limit = 30
        self.request_limit = 3

        self.logger = self._get_logger()

        self.init_http_limit(app)
        return app     

    def _view(self):
        return "test", HTTPStatus.OK

    def _get_logger(self):
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

        return logger


class TestHttpLimitIntegratedWithoutFilters(BaseHttpLimitIntegratedTest):

    def init_http_limit(self, app):
        limit_by_time_rule = LimitByTimeRule(self.redis_client, self.time_limit, self.request_limit, logger=self.logger)
        ip_uid_provider = IpUidProvider(logger=self.logger)        
        http_limit = HttpLimit(app, ip_uid_provider, [limit_by_time_rule], logger=self.logger)
    
    def test_should_run_when_execution_count_not_exceeded(self):

        for i in range(0,self.request_limit):
            response = requests.get(self.get_server_url())
            response.status_code | should.be.equal.to(HTTPStatus.OK)        

    def test_should_return_TOO_MANY_REQUESTS_when_execution_count_exceeded(self):        
        for i in range(0,self.request_limit):
            response = requests.get(self.get_server_url())
            response.status_code | should.be.equal.to(HTTPStatus.OK)

        response = requests.get(self.get_server_url())
        response.status_code | should.be.equal.to(HTTPStatus.TOO_MANY_REQUESTS)
        response.text | should.match("Rate limit exceeded. Try again in \d+ seconds.")

    def test_should_reset_limit_when_execution_count_exceeded(self):        
        for i in range(0,self.request_limit):
            response = requests.get(self.get_server_url())
            response.status_code | should.be.equal.to(HTTPStatus.OK)

        time.sleep(self.time_limit)

        response = requests.get(self.get_server_url())
        response.status_code | should.be.equal.to(HTTPStatus.OK)

class TestHttpLimitIntegratedWithIpFilter(BaseHttpLimitIntegratedTest):

    def init_http_limit(self, app):
        limit_by_time_rule = LimitByTimeRule(self.redis_client, self.time_limit, self.request_limit, logger=self.logger)
        ip_uid_provider = IpUidProvider(logger=self.logger)        
        filter = IpFilter(ips=["127.0.0.1"])
        http_limit = HttpLimit(app, ip_uid_provider, [limit_by_time_rule], filters=[filter], logger=self.logger)

    def test_should_ignore_rules_when_filters_match(self):

        for i in range(0,self.request_limit + 1):
            response = requests.get(self.get_server_url())
            response.status_code | should.be.equal.to(HTTPStatus.OK)

class TestHttpLimitIntegratedWithOneMatchingFilterOfTwo(BaseHttpLimitIntegratedTest):

    def init_http_limit(self, app):
        limit_by_time_rule = LimitByTimeRule(self.redis_client, self.time_limit, self.request_limit, logger=self.logger)
        ip_uid_provider = IpUidProvider(logger=self.logger)        
        ip_filter = IpFilter(ips=["127.0.0.1"])
        route_filter = RouteFilter("test",logger=self.logger)
        http_limit = HttpLimit(app, ip_uid_provider, [limit_by_time_rule], filters=[ip_filter, route_filter], logger=self.logger)

    def test_should_ignore_rules_when_filters_match(self):

        for i in range(0,self.request_limit + 1):
            response = requests.get(self.get_server_url())
            response.status_code | should.be.equal.to(HTTPStatus.OK)

class TestHttpLimitIntegratedWithRouteFilterForIndexRoute(BaseHttpLimitIntegratedTest):

    def init_http_limit(self, app):        
        limit_by_time_rule = LimitByTimeRule(self.redis_client, self.time_limit, self.request_limit, logger=self.logger)
        ip_uid_provider = IpUidProvider(logger=self.logger)        
        route_filter = RouteFilter("index", logger=self.logger)
        http_limit = HttpLimit(app, ip_uid_provider, [limit_by_time_rule], filters=[route_filter], logger=self.logger)

    def test_should_ignore_rules_when_filters_match(self):

        for i in range(0,self.request_limit + 1):
            response = requests.get(self.get_server_url())
            response.status_code | should.be.equal.to(HTTPStatus.OK)

class TestHttpLimitIntegratedWithRouteFilterForTestRoute(BaseHttpLimitIntegratedTest):

    def init_http_limit(self, app):
        limit_by_time_rule = LimitByTimeRule(self.redis_client, self.time_limit, self.request_limit, logger=self.logger)
        ip_uid_provider = IpUidProvider(logger=self.logger)        
        route_filter = RouteFilter("test", logger=self.logger)
        http_limit = HttpLimit(app, ip_uid_provider, [limit_by_time_rule], filters=[route_filter], logger=self.logger)

    def test_should_ignore_rules_when_filters_match(self):

        for i in range(0,self.request_limit + 1):
            response = requests.get(self.get_server_url() + "/test")
            response.status_code | should.be.equal.to(HTTPStatus.OK)
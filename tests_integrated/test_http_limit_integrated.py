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

from flask_http_limit import HttpLimit, LimitByTimeRule, IpUidProvider

class TestHttpLimitIntegrated(LiveServerTestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 5000
        app.config['LIVESERVER_TIMEOUT'] = 10

        app.add_url_rule("/", view_func=self._view)

        logger = self._get_logger()

        redis_client = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
        redis_client.flushdb()
        self.time_limit = 30
        self.request_limit = 3
        limit_by_time_rule = LimitByTimeRule(redis_client, self.time_limit, self.request_limit, logger=logger)
        ip_uid_provider = IpUidProvider(logger=logger)
        http_limit = HttpLimit(app, [limit_by_time_rule], ip_uid_provider, logger=logger)

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
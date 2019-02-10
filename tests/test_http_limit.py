"""
Unit tests for HttpLimit extension
"""

from flask import Flask
from flask.json import jsonify
from grappa import should
from http import HTTPStatus

from flask_http_limit import HttpLimit
from mocks import MockRule, MockUidProvider, MockFilter

class TestHttpLimit():
    def setup_method(self):
        self.app = app = Flask("test")
        self.app.add_url_rule("/", view_func=self._view)
        self.mock_uid_provider = MockUidProvider(uid="mock")

    def _view(self):
        return "test", HTTPStatus.OK

    def test_should_execute_before_every_request_when_app_in_constructor(self):
        mock_rule = MockRule(should_execute=True)        
        HttpLimit(self.app, self.mock_uid_provider, [mock_rule])

        client = self.app.test_client()
        response = client.get("/")

        response.status_code | should.be.equal.to(HTTPStatus.OK)
        mock_rule.apply_called | should.be.true
        self.mock_uid_provider.get_uid_called | should.be.true

    def test_should_execute_before_every_request_when_initializes_app(self):        
        mock_rule = MockRule(should_execute=True)        
        http_limit = HttpLimit(None, self.mock_uid_provider, [mock_rule])
        http_limit.init_app(self.app)

        client = self.app.test_client()
        response = client.get("/")

        response.status_code | should.be.equal.to(HTTPStatus.OK)
        mock_rule.apply_called | should.be.true
        self.mock_uid_provider.get_uid_called | should.be.true

    def test_should_return_error_status_code_when_limit_exceded(self):
        status_code = 400        
        mock_rule = MockRule(should_execute=False, status_code=status_code)        
        http_limit = HttpLimit(None, self.mock_uid_provider, [mock_rule])
        http_limit.init_app(self.app)

        client = self.app.test_client()
        response = client.get("/")

        response.status_code | should.be.equal.to(status_code)
        mock_rule.apply_called | should.be.true
        self.mock_uid_provider.get_uid_called | should.be.true

    def test_should_apply_rules_when_filters_match(self):
        mock_rule = MockRule(should_execute=True)
        mock_filter = MockFilter(ignore=False)
        http_limit = HttpLimit(None, self.mock_uid_provider, [mock_rule], filters=[mock_filter])
        http_limit.init_app(self.app)

        client = self.app.test_client()
        response = client.get("/")

        response.status_code | should.be.equal.to(HTTPStatus.OK)
        mock_filter.ignore_called | should.be.true
        mock_rule.apply_called | should.be.true

    def test_should_ignore_rules_when_filters_do_not_match(self):
        mock_rule = MockRule(should_execute=True)
        mock_filter = MockFilter(ignore=True)
        http_limit = HttpLimit(None, self.mock_uid_provider, [mock_rule], filters=[mock_filter])
        http_limit.init_app(self.app)

        client = self.app.test_client()
        response = client.get("/")

        response.status_code | should.be.equal.to(HTTPStatus.OK)
        mock_filter.ignore_called | should.be.true
        mock_rule.apply_called | should.be.false        
        

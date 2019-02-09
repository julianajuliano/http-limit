from flask import Flask
from grappa import should

from flask_http_limit import HttpLimit
from mocks import MockRule, MockUidProvider

class TestHttpLimit():
    def test_should_execute_before_every_request_when_app_in_constructor(self):
        app = Flask("test")
        mock_rule = MockRule()
        mock_uid_provider = MockUidProvider()
        HttpLimit(app, mock_rule, mock_uid_provider)

        client = app.test_client()
        client.get("/")

        mock_rule.can_execute_called | should.be.true
        mock_uid_provider.get_uid_called | should.be.true

    def test_should_execute_before_every_request_when_initializes_app(self):
        app = Flask("test")
        mock_rule = MockRule()
        mock_uid_provider = MockUidProvider()
        http_limit = HttpLimit(None, mock_rule, mock_uid_provider)
        http_limit.init_app(app)

        client = app.test_client()
        client.get("/")

        mock_rule.can_execute_called | should.be.true
        mock_uid_provider.get_uid_called | should.be.true
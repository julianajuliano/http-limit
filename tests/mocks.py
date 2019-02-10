"""
Mock clases to be used in unit testing.
"""
from datetime import datetime, timedelta
from unittest.mock import MagicMock, PropertyMock

from flask_http_limit import HttpLimitError

class MockRedisClient():
    def __init__(self):
        self.key_store = {}
        self.key_expires = {}

    def get(self, key):
        if key not in self.key_store:
            return None
        
        if datetime.utcnow() > self.key_expires[key]:
            return None
        
        return self.key_store[key]

    def set(self, key, value, ex):
        self.key_store[key] = value
        self.key_expires[key] = datetime.utcnow() + timedelta(seconds=ex)
    
    def incr(self, key):
        self.key_store[key] = self.key_store[key] + 1
        print(self.key_store[key])

    def ttl(self, key):
        time_delta = self.key_expires[key] - datetime.utcnow()
        return int(time_delta.total_seconds())

class MockRequest():
    def __init__(self, ip = None, x_fowarded = [], route = None):
        self.ip = ip
        
        self.headers = MagicMock()
        if len(x_fowarded) > 0:
            self.headers.getlist.return_value = x_fowarded
        else:
            self.headers.getlist.return_value = None

        self.url_rule = MagicMock()        
        self.url_rule.endpoint = route

    @property
    def remote_addr(self):
        return self.ip

class MockRule():
    def __init__(self, should_execute, status_code=0):
        self.should_execute = should_execute
        self.status_code = status_code
        self.apply_called = False
    
    def apply(self, uid):
        self.apply_called = True
        if not self.should_execute:
            raise HttpLimitError(self.status_code, "error")

class MockIpResolver():
    def __init__(self, ip):
        self.get_ip_called = False
        self.ip = ip
    
    def get_ip(self, request):
        self.get_ip_called = True
        return self.ip

class MockUidProvider():
    def __init__(self, uid):
        self.get_uid_called = False
        self.uid = uid
    
    def get_uid(self, request):
        self.get_uid_called = True
        return self.uid

class MockFilter():
    def __init__(self, ignore):
        self.ignore_called = False
        self.ignore_result = ignore
    
    def ignore(self, request):
        self.ignore_called = True
        return self.ignore_result
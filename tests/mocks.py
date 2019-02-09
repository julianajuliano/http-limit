from datetime import datetime, timedelta
from unittest.mock import MagicMock

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

class MockRequest():
    def __init__(self, ip, x_fowarded = []):
        self.ip = ip
        self.headers = MagicMock()

        if len(x_fowarded) > 0:
            self.headers.getlist.return_value = x_fowarded
        else:
            self.headers.getlist.return_value = None

    @property
    def remote_addr(self):
        return self.ip

class MockRule():
    def __init__(self):
        self.can_execute_called = False
    
    def can_execute(self, uid):
        self.can_execute_called = True
        return True

class MockUidProvider():
    def __init__(self):
        self.get_uid_called = False
    
    def get_uid(self, request):
        self.get_uid_called = True
        return "mock"

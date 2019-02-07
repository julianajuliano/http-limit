from flask import current_app

class HttpLimit():
    def __init__(self, app, limit_rule, uid_provider):        
        self.app = app
        self.limit_rule = limit_rule
        self.uid_provider = limit_rule

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        pass

    def can_execute(self):
        return self.limit_rule.can_execute(uid_provider.get_uid())

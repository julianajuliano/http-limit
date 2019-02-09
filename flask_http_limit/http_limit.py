from flask import current_app, request

class HttpLimit():
    """Flask Http Request Limit extension

    Methods:
        init_app
        can_execute
    """
    def __init__(self, app, limit_rule, uid_provider):
        """
        Initializes extension.
        
        Arguments:
            app: flask application object
            limit_rule: limit rule implementation
            uid_provider: unique id provider
        """
        self.app = app
        self.limit_rule = limit_rule
        self.uid_provider = uid_provider

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes app, to be used in multi Flask application scenarios.
        """
        app.before_request(self._can_execute)

    def _can_execute(self):
        """
        Execute the rule passing it the uid generatd by the provider. 

        Returns:
            True if requester can execute.
            False if requester has reached the rule limit.
        """
        app = self._get_app()
        with app.app_context():
            return self.limit_rule.can_execute(self.uid_provider.get_uid(request))

    def _get_app(self):
        """
        Get the current running flask app.
        """
        if self.app:
            return self.app

        return current_app
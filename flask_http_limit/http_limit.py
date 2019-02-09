from flask import abort, current_app, request, Response

class HttpLimit():
    """Flask Http Request Limit extension

    Methods:
        init_app
        _limit_request
        _get_app
    """
    def __init__(self, app, rules, uid_provider):
        """
        Initializes extension.
        
        Arguments:
            app: flask application object
            rules: array of rules to be applied
            uid_provider: unique id provider
        """
        self.app = app
        self.rules = rules
        self.uid_provider = uid_provider

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes app, to be used in multi Flask application scenarios.
        """
        app.before_request(self._limit_request)

    def _limit_request(self):
        """
        Execute the rule passing it the uid generatd by the provider. 

        Returns:
            True if requester can execute.
            False if requester has reached the rule limit.
        """
        app = self._get_app()
        with app.app_context():
            for rule in self.rules:
                try:
                    rule.apply(self.uid_provider.get_uid(request))
                except HttpLimitError as ex:
                    abort(ex.status_code, ex.message)

    def _get_app(self):
        """
        Get the current running flask app.
        """
        if self.app:
            return self.app

        return current_app

class HttpLimitError(Exception):
    """
    Error to report that the limit defined be the rule has been reached.
    """
    def __init__(self, status_code, message):
        """
        Initializes exception.
        
        Arguments:
            status_code: http status code
            msmessageg: error message to be returned
        """
        self.status_code = status_code
        self.message = message
        super(HttpLimitError, self).__init__(self.message)
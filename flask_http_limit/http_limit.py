import logging
from flask import abort, current_app, request, Response

class HttpLimit():
    """Flask Http Request Limit extension

    Methods:
        init_app
    """
    def __init__(self, app, uid_provider, rules, logger=None):
        """
        Initialize extension.
        
        Arguments:
            app: flask application object
            uid_provider: unique id provider
            rules: array of rules to be applied            
            logger: logger instance of python's standard logging library
        """
        self.app = app
        self.rules = rules
        self.uid_provider = uid_provider
        self.logger = logger or logging.getLogger(__name__)

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes app, to be used in multi Flask application scenarios.
        """
        self.logger.debug("init_app called")
        
        app.before_request(self._limit_request)
        
        self.logger.debug("init_app finished")

    def _limit_request(self):
        """
        Execute the limit rules passing the uid generatd by the provider.         
        """
        self.logger.debug("_limit_request called")
        app = self._get_app()
        with app.app_context():
            for rule in self.rules:
                try:
                    rule.apply(self.uid_provider.get_uid(request))
                    self.logger.debug("_limit_request finished")

                except HttpLimitError as ex:
                    self.logger.error("HttpLimitError raised, aborting request with status code {status}".format(status=ex.status_code))
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
    Error to report the limit defined by the rule has been reached.
    """
    def __init__(self, status_code, message):
        """
        Initializes error.
        
        Arguments:
            status_code: http status code
            msmessageg: error message to be returned
        """
        self.status_code = status_code
        self.message = message
        super(HttpLimitError, self).__init__(self.message)
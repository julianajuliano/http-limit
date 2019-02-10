# Flask-HttpLimit
Http limit flask extension for python 

![[CircleCI](https://circleci.com/gh/julianajuliano/http-limit/tree/master.svg?style=svg)

# Introduction
Flask-HttpLimit lets you easily plugin request limiting rules to your [Flask](http://flask.pocoo.org/) apps.

## Requirements
Python 3.7+

# TO-DO DOCUMENT WHAT IS SHIPPED

# Installation
This extension is not availabile in a pip package, so clone the repository and run the following commands:

    git clone https://github.com/julianajuliano/http-limit.git
    cd http-limit
    python -m venv env
    .\env\scripts\activate.ps1 (Windows) | .\env\bin\activate (Linux)
    python setup.py install


# Installation-Dev
For dev and testing purposes, run the following after running install

    pip install -e ".[test]"

You can also run *INSTALL-DEV.ps1* if you are running on Windows+Powershell

# Example

    app = Flask("myapp")
   
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    redis_client = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
   
    self.time_limit = 3600 # request limit expires every hour
    self.request_limit = 100 # 100 requests per hour
    limit_by_time_rule = LimitByTimeRule(redis_client, self.time_limit, self.request_limit, logger=logger)
    ip_uid_provider = IpUidProvider(logger=logger)
    http_limit = HttpLimit(app, [limit_by_time_rule], ip_uid_provider, logger=logger)

# Extending functionality
It is possible to increment Flask-HttpLimit extension with your on rules. 

## Implementing a different UID provider
**UID** refers to the unique id of the request, it is based on this value that the limiting rule will be applied. You can create your own UID provider and pass it on to the HttpLimit extension.

### UidProvider interface
UidProvider requires a get_uid function that receives a parameter. The flask request context will be passed to get_uid so you can decide on how to calculate your UID. 

    get_uid(request):

## Implementing a different Rule
Flask-HttpLimit extension can deal with more than one rule at time. It receives an array of rules and applies them in order. You can write your own rule that adds functionality to the built-in rule or you can create one from scratch and use only your custom rule.

### Rule Interface
Rule requires an apply function that receives the uid. If the limit has been reached you need to raise an HttpLimitError passing the HttpStatus code you want to return to flask and an error message.

    apply(uid); 
    raises HttpLimitError

# Logging
This extension uses python's standard logging library, it emits DEBUG and ERROR level messages. For more info on how to configure your application for logging visit [official documentation](https://docs.python.org/3/library/logging.html)

# Tests
Testes are run with [pytest](https://docs.pytest.org/en/latest/). 

## Requirements
Integration tests requires local running [redis](https://hub.docker.com/_/redis). You can use docker's redis image:

    docker pull redis
    docker run -d -p 6379:6379 -i -t redis:latest --name local-redis

## Runnings tests

### Running all tests:

    python setup.py test

### Running unit tests only

    pytest tests

### Running integration tests only

    pytest tests_integrated

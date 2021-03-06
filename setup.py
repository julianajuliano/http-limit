"""
Flask-HttpLimit

Adds request limiting feature to flask.

"""

from setuptools import setup

requires = [
    "redis",
    "Flask"
]
test_requires = [
    "pytest",
    "grappa" ,
    "Flask-Testing",
    "requests"
]

setup(
    name = "Flask-HttpLimit",
    version = "1.0.0",
    url = "https://github.com/julianajuliano/http-limit",
    author = "Juliana Juliano",
    author_email = "julianajuliano@gmail.com",
    description = ("Limit HTTP requests."),
    packages=["flask_http_limit"],
    install_requires=requires,
    setup_requires="pytest-runner",
    extras_require= {
        "test": test_requires
    },
    test_requires=test_requires,
    test_suit="pytest",  
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
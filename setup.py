from setuptools import setup

requires = [
    "redis"    
]

test_requires = [
    "pytest",
    "grappa"    
]

setup(
    name = "http_limit",
    version = "0.0.0",
    author = "Juliana Juliano",
    author_email = "julianajuliano@gmail.com",
    description = ("Limit HTTP requests."),
    packages=["http_limit"],
    install_requires=requires,
    extras_require= {
        "test": test_requires
    }
)
"""
# Flask-Shell2HTTP

A minimalist REST API wrapper for python's subprocess API.<br/>
Execute shell commands asynchronously and safely from flask's endpoints.

##### Docs & Example usage on GitHub: https://github.com/eshaan7/flask-shell2http
"""
import pathlib
from setuptools import setup

# The text of the README file
README = (pathlib.Path(__file__).parent / "README.md").read_text()

GITHUB_URL = "https://github.com/eshaan7/flask-shell2http"


setup(
    name="Flask-Shell2HTTP",
    version="1.6.0",
    url=GITHUB_URL,
    license="BSD",
    author="Eshaan Bansal",
    author_email="eshaan7bansal@gmail.com",
    description="A minimalist REST API wrapper for python's subprocess API.",
    long_description=README,
    long_description_content_type="text/markdown",
    py_modules=["flask_shell2http"],
    zip_safe=False,
    packages=["flask_shell2http"],
    include_package_data=True,
    platforms="any",
    python_requires=">= 3.6",
    install_requires=["Flask", "Flask-Executor"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="flask shell2http subprocess python",
    project_urls={
        "Documentation": GITHUB_URL,
        "Funding": "https://www.paypal.me/eshaanbansal",
        "Source": GITHUB_URL,
        "Tracker": "{}/issues".format(GITHUB_URL),
    },
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        "test": [
            "flask_testing",
            "black==20.8b1",
            "flake8",
            "nose",
            "blinker",
            "requests",
            "codecov",
        ],
    },
)

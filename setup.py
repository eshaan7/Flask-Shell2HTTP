"""
# Flask-Shell2HTTP

A minimalist REST API wrapper for python's subprocess API.<br/>
Execute shell commands asynchronously and safely from flask's endpoints.

##### Docs & Example usage on GitHub: https://github.com/eshaan7/flask-shell2http
"""
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# version
VERSION = (HERE / "version.txt").read_text()

GITHUB_URL = "https://github.com/eshaan7/flask-shell2http"

requirements = (HERE / "requirements.txt").read_text().split("\n")

requirements_test = (HERE / "requirements.dev.txt").read_text().split("\n")

# This call to setup() does all the work
setup(
    name="Flask-Shell2HTTP",
    version=VERSION,
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
    install_requires=requirements,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
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
        "test": requirements + requirements_test,
    },
)

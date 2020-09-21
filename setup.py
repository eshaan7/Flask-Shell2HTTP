"""
# Flask-Shell2HTTP

A minimalist REST API wrapper for python's subprocess API.<br/>
Execute shell commands asynchronously and safely from flask's endpoints.

##### Docs & Example usage on GitHub: https://github.com/eshaan7/flask-shell2http
"""
from setuptools import setup


with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

GITHUB_URL = "https://github.com/eshaan7/flask-shell2http"


setup(
    name="Flask-Shell2HTTP",
    version="1.5.0",
    url=GITHUB_URL,
    license="BSD",
    author="Eshaan Bansal",
    author_email="eshaan7bansal@gmail.com",
    description="A minimalist REST API wrapper for python's subprocess API.",
    long_description=long_description,
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
)

# Flask-Shell2HTTP

[![CodeFactor](https://www.codefactor.io/repository/github/eshaan7/flask-shell2http/badge)](https://www.codefactor.io/repository/github/eshaan7/flask-shell2http)
<a href="https://lgtm.com/projects/g/eshaan7/flask-shell2http/context:python">
  <img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/eshaan7/flask-shell2http.svg?logo=lgtm&logoWidth=18"/>
</a>
[![flask-shell2http on pypi](https://img.shields.io/pypi/v/flask-shell2http)](https://pypi.org/project/Flask-Shell2HTTP/)

A minimalist [Flask](https://github.com/pallets/flask) extension that serves as a REST API wrapper for python's subprocess API.

- **Convert any command-line tool into a REST API service.**
- Execute pre-defined shell commands asynchronously and securely via flask's endpoints.
- Designed for development, prototyping or remote control.

Inspired by the work of awesome folks over at [msoap/shell2http](https://github.com/msoap/shell2http).

## Use Cases

- Set a script that runs on a succesful POST request to an endpoint of your choice. See [Example code](examples/run_script.py).
- Map a base command to an endpoint and pass dynamic arguments to it. See [Example code](examples/basic.py).
- Can also process multiple uploaded files in one command. See [Example code](examples/multiple_files.py).
- This is useful for internal docker-to-docker communications if you have lots of different binaries. See [real-life example](https://github.com/intelowlproject/IntelOwl/blob/develop/integrations/peframe/app.py).
- Currently, all commands are run asynchronously, so result is not available directly. An option would be provided for this in future release.

> Note: This extension is primarily meant for executing long-running
> shell commands/scripts (like nmap, code-analysis' tools) in background from an HTTP request and getting the result at a later time.

## Documentation / Quick Start

[![Documentation Status](https://readthedocs.org/projects/flask-shell2http/badge/?version=latest)](https://flask-shell2http.readthedocs.io/en/latest/?badge=latest)

Read the [Quickstart](https://flask-shell2http.readthedocs.io/quickstart.html) 
from the [documentation](https://flask-shell2http.readthedocs.io/) to get started!

## Why?

This was initially made to integrate various command-line tools easily with [IntelOwl](https://github.com/intelowlproject/IntelOwl).


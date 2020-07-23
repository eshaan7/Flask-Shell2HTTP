# Flask-Shell2HTTP

[![CodeFactor](https://www.codefactor.io/repository/github/eshaan7/flask-shell2http/badge)](https://www.codefactor.io/repository/github/eshaan7/flask-shell2http)
<a href="https://lgtm.com/projects/g/Eshaan7/Flask-Shell2HTTP/context:python">
  <img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/Eshaan7/Flask-Shell2HTTP.svg?logo=lgtm&logoWidth=18"/>
</a>
[![flask-shell2http on pypi](https://img.shields.io/pypi/v/flask-shell2http)](https://pypi.org/project/Flask-Shell2HTTP/)

A minimalist [Flask](https://github.com/pallets/flask) extension that serves as a RESTful/HTTP wrapper for python's subprocess API.

- **Convert any command-line tool into a REST API service.**
- Execute pre-defined shell commands asynchronously and securely via flask's endpoints with dynamic arguments, file upload, callback function capabilities.
- Designed for binary to binary/HTTP communication, development, prototyping, remote control and [more](https://flask-shell2http.readthedocs.io/en/stable/Examples.html).


## Use Cases

- Set a script that runs on a succesful POST request to an endpoint of your choice. See [Example code](examples/run_script.py).
- Map a base command to an endpoint and pass dynamic arguments to it. See [Example code](examples/basic.py).
- Can also process multiple uploaded files in one command. See [Example code](examples/multiple_files.py).
- This is useful for internal docker-to-docker communications if you have different binaries distributed in micro-containers. See [real-life example](https://github.com/intelowlproject/IntelOwl/blob/develop/integrations/peframe/app.py).
- You can define a callback function/ use signals to listen for process completion. See [Example code](examples/with_callback.py). 
  * Maybe want to pass some additional context to the callback function ? 
  * Maybe intercept on completion and update the result ? See [Example code](examples/custom_save_fn.py)
- Currently, all commands run asynchronously (default timeout is 3600 seconds), so result is not available directly. An option _may_ be provided for this in future releases for commands that return immediately.

> Note: This extension is primarily meant for executing long-running
> shell commands/scripts (like nmap, code-analysis' tools) in background from an HTTP request and getting the result at a later time.

## Documentation / Quick Start

[![Documentation Status](https://readthedocs.org/projects/flask-shell2http/badge/?version=latest)](https://flask-shell2http.readthedocs.io/en/latest/?badge=latest)

Read the [Quickstart](https://flask-shell2http.readthedocs.io/en/stable/Quickstart.html) 
from the [documentation](https://flask-shell2http.readthedocs.io/) to get started!

I highly recommend the [Examples](https://flask-shell2http.readthedocs.io/en/stable/Examples.html) section.

## Inspiration

This was initially made to integrate various command-line tools easily with [Intel Owl](https://github.com/intelowlproject/IntelOwl), which I am working on as part of Google Summer of Code.

The name was inspired by the awesome folks over at [msoap/shell2http](https://github.com/msoap/shell2http).

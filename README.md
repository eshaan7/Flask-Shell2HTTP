[![Get Support](https://xscode.com/assets/promo-banner.svg)](https://xscode.com/eshaan7/Flask-Shell2HTTP)

_For urgent issues and priority support, visit [https://xscode.com/eshaan7/flask-shell2http](https://xscode.com/eshaan7/flask-shell2http)._

# Flask-Shell2HTTP

[![flask-shell2http on pypi](https://img.shields.io/pypi/v/flask-shell2http)](https://pypi.org/project/Flask-Shell2HTTP/)
[![Build Status](https://github.com/Eshaan7/flask-shell2http/workflows/Linter%20&%20Tests/badge.svg?branch=master)](https://github.com/Eshaan7/flask-shell2http/actions?query=workflow%3A%22Linter+%26+Tests%22)
[![codecov](https://codecov.io/gh/Eshaan7/Flask-Shell2HTTP/branch/master/graph/badge.svg?token=UQ43PYQPMR)](https://codecov.io/gh/Eshaan7/flask-shell2http/)
[![CodeFactor](https://www.codefactor.io/repository/github/eshaan7/flask-shell2http/badge)](https://www.codefactor.io/repository/github/eshaan7/flask-shell2http)
<a href="https://lgtm.com/projects/g/Eshaan7/Flask-Shell2HTTP/context:python">
  <img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/Eshaan7/Flask-Shell2HTTP.svg?logo=lgtm&logoWidth=18"/>
</a>

A minimalist [Flask](https://github.com/pallets/flask) extension that serves as a RESTful/HTTP wrapper for python's subprocess API.

- **Convert any command-line tool into a REST API service.**
- Execute pre-defined shell commands asynchronously and securely via flask's endpoints with dynamic arguments, file upload, callback function capabilities.
- Designed for binary to binary/HTTP communication, development, prototyping, remote control and [more](https://flask-shell2http.readthedocs.io/en/stable/Examples.html).


## Use Cases

- Set a script that runs on a succesful POST request to an endpoint of your choice. See [Example code](examples/run_script.py).
- Map a base command to an endpoint and pass dynamic arguments to it. See [Example code](examples/basic.py).
- Can also process multiple uploaded files in one command. See [Example code](examples/multiple_files.py).
- This is useful for internal docker-to-docker communications if you have different binaries distributed in micro-containers. See [real-life example](https://github.com/intelowlproject/IntelOwl/blob/master/integrations/static_analyzers/app.py).
- You can define a callback function/ use signals to listen for process completion. See [Example code](examples/with_callback.py). 
  * Maybe want to pass some additional context to the callback function ? 
  * Maybe intercept on completion and update the result ? See [Example code](examples/custom_save_fn.py)
- You can also apply [View Decorators](https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/) to the exposed endpoint. See [Example code](examples/with_decorators.py).
- Currently, all commands run asynchronously (default timeout is 3600 seconds), so result is not available directly. An option _may_ be provided for this in future releases for commands that return immediately.

> Note: This extension is primarily meant for executing long-running
> shell commands/scripts (like nmap, code-analysis' tools) in background from an HTTP request and getting the result at a later time.


## Documentation

[![Documentation Status](https://readthedocs.org/projects/flask-shell2http/badge/?version=latest)](https://flask-shell2http.readthedocs.io/en/latest/?badge=latest)

- Read the [Quickstart](https://flask-shell2http.readthedocs.io/en/stable/Quickstart.html) from the [documentation](https://flask-shell2http.readthedocs.io/) to get started!
- I also highly recommend the [Examples](https://flask-shell2http.readthedocs.io/en/stable/Examples.html) section.
- [CHANGELOG](https://github.com/eshaan7/Flask-Shell2HTTP/blob/master/.github/CHANGELOG.md).


## Quick Start

##### Dependencies

* Python: `>=v3.6`
* [Flask](https://pypi.org/project/Flask/)
* [Flask-Executor](https://pypi.org/project/Flask-Executor)

##### Installation

```bash
$ pip install flask flask_shell2http
```

##### Example Program

Create a file called `app.py`.

```python
from flask import Flask
from flask_executor import Executor
from flask_shell2http import Shell2HTTP

# Flask application instance
app = Flask(__name__)

executor = Executor(app)
shell2http = Shell2HTTP(app=app, executor=executor, base_url_prefix="/commands/")

def my_callback_fn(context, future):
  # optional user-defined callback function
  print(context, future.result())

shell2http.register_command(endpoint="saythis", command_name="echo", callback_fn=my_callback_fn, decorators=[])
```

Run the application server with, `$ flask run -p 4000`.

With <10 lines of code, we succesfully mapped the shell command `echo` to the endpoint `/commands/saythis`.

##### Making HTTP calls

This section demonstrates how we can now call/ execute commands over HTTP that we just mapped in the [example](#example-program) above.

```bash
$ curl -X POST -H 'Content-Type: application/json' -d '{"args": ["Hello", "World!"]}' http://localhost:4000/commands/saythis
```

<details><summary>or using python's requests module,</summary>

```python
# You can also add a timeout if you want, default value is 3600 seconds
data = {"args": ["Hello", "World!"], "timeout": 60}
resp = requests.post("http://localhost:4000/commands/saythis", json=data)
print("Result:", resp.json())
```

</details>

> Note: You can see the JSON schema for the POST request [here](https://github.com/Eshaan7/Flask-Shell2HTTP/blob/master/post-request-schema.json).

returns JSON,

```json
{
   "key": "ddbe0a94",
   "result_url": "http://localhost:4000/commands/saythis?key=ddbe0a94&wait=false",
   "status": "running"
}
```

Then using this `key` you can query for the result or just by going to the `result_url`,

```bash
$ curl http://localhost:4000/commands/saythis?key=ddbe0a94&wait=true # wait=true so we do not have to poll
```

Returns result in JSON,

```json
{
  "report": "Hello World!\n",
  "key": "ddbe0a94",
  "start_time": 1593019807.7754705,
  "end_time": 1593019807.782958,
  "process_time": 0.00748753547668457,
  "returncode": 0,
  "error": null,
}
```


## Inspiration

This was initially made to integrate various command-line tools easily with [Intel Owl](https://github.com/intelowlproject/IntelOwl), which I am working on as part of Google Summer of Code.

The name was inspired by the awesome folks over at [msoap/shell2http](https://github.com/msoap/shell2http).

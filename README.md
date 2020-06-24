# Flask-Shell2HTTP

[![flask-shell2http on pypi](https://img.shields.io/pypi/v/flask-shell2http)](https://pypi.org/project/Flask-Shell2HTTP/)

A minimalist [Flask](https://github.com/pallets/flask) extension that serves as a REST API wrapper for python's subprocess API.<br/>

- **Convert any command-line tool into a REST API service.**
- Execute shell commands asynchronously and safely from flask's endpoints.

Inspired by the work of awesome folks over at [msoap/shell2http](https://github.com/msoap/shell2http).

## Use Cases

- Set a script that runs on a succesful POST request to an endpoint of your choice. See [Example code](examples/run_script.py).
- Map a base command to an endpoint and pass dynamic arguments to it. See [Example code](examples/basic.py).
- Can also process multiple uploaded files in one command. See [Example code](examples/multiple_files.py).
- Currently, all commands are run asynchronously, so result is not available directly. An option would be provided for this in future release.

> Note: This module is primarily meant for running long-running shell commands/scripts (like nmap, code-analysis' tools) in background and getting the result at a later time.

## Quick Start

#### Dependencies

- Python: `>=v3.6`
- [Flask](https://pypi.org/project/Flask/)
- [Flask-Executor](https://pypi.org/project/Flask-Executor)

#### Install

```bash
$ pip install flask flask_shell2http
```

#### Example

```python
from flask import Flask
from flask_executor import Executor
from flask_shell2http import Shell2HTTP

# Flask application instance
app = Flask(__name__)

executor = Executor(app)
shell2http = Shell2HTTP(app=app, executor=executor, base_url_prefix="/commands/")

shell2http.register_command(endpoint="saythis", command_name="echo")
```

Run the application server with, `$ flask run -p 4000`.

#### Make HTTP calls

```bash
$ curl -X POST -d '{"args": ["Hello", "World!"]}' http://localhost:4000/commands/saythis
```

<details><summary>or using python's requests module,</summary>

```python
data = {"args": ["Hello", "World!"]}
resp = requests.post("http://localhost:4000/commands/saythis", json=data)
print("Result:", resp.json())
```

</details>

returns JSON,

```json
{
   "key": "ddbe0a94847c65f9b8198424ffd07c50",
   "status": "running"
}
```

Then using this `key` you can query for the result,

```bash
$ curl http://localhost:4000/commands/saythis?key=ddbe0a94847c65f9b8198424ffd07c50
```

Returns result in JSON,

```json
{
  "end_time": 1593019807.782958, 
  "error": "", 
  "md5": "ddbe0a94847c65f9b8198424ffd07c50", 
  "process_time": 0.00748753547668457, 
  "report": {
    "result": "Hello World!\n"
  }, 
  "start_time": 1593019807.7754705, 
  "status": "success"
}
```

## Why?

This was initially made to integrate various command-line tools easily with [IntelOwl](https://github.com/intelowlproject/IntelOwl).

## Example usage

You can find various examples under [examples](examples/).

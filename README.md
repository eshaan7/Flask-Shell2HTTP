# Flask-Shell2HTTP

A minimalist REST API wrapper for python's subprocess API.<br/>
Execute shell commands asynchronously and safely from flask's endpoints.

Inspired by the work of awesome folks over at [msoap/shell2http](https://github.com/msoap/shell2http).

## You can use this for

- Set a script that runs on a succesful POST request to an endpoint of your choice. See [Example code](examples/run_script.py)
- Map a base command to an endpoint and passing dynamic arguments to it. See [Example code](examples/basic.py)
- Can also process uploaded files. See [Example code](examples/multiple_files.py)
- Choose to run a command asynchronously or not. (upcoming feature)

## Quick Start

#### Dependencies

- Python: `>=v3.6`
- [Flask](https://pypi.org/project/Flask/)
- [Flask-Executor](https://pypi.org/project/Flask-Executor)

#### Install

```bash
$ pip install flask_shell2http flask_executor
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

This was made to integrate various command-line tools easily with [IntelOwl](https://github.com/intelowlproject/IntelOwl).

## Various examples

You can find various examples under [examples](examples/)
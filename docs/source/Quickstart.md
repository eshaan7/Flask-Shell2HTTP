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

shell2http.register_command(endpoint="saythis", command_name="echo")
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

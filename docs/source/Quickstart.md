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
   "result_url": "http://localhost:4000/commands/saythis?key=ddbe0a94",
   "status": "running"
}
```

Then using this `key` you can query for the result or just by going to the `result_url`,

```bash
$ curl http://localhost:4000/commands/saythis?key=ddbe0a94
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

##### Bonus

You can also define callback functions or use signals for reactive programming. There may be cases where the process doesn't print result to standard output but to a file/database. In such cases, you may want to intercept the future object and update it's result attribute.
I request you to take a look at [Examples.md](Examples.md) for such use-cases.
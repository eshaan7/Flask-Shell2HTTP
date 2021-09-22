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
data = {"args": ["Hello", "World!"], "timeout": 60, "force_unique_key": False}
resp = requests.post("http://localhost:4000/commands/saythis", json=data)
print("Result:", resp.json())
```

</details>

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
$ curl http://localhost:4000/commands/saythis?key=ddbe0a94&wait=true # wait=true so we don't need to poll
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

<div id="hint-wait" class="admonition hint">
<p class="admonition-title">Hint</p>
Use <code>wait=true</code> when you don't wish to HTTP poll and want the result in a single request only.
This is especially ideal in case you specified a low <code>timeout</code> value in the <code>POST</code> request.
</div>


<div id="hint-key" class="admonition hint">
<p class="admonition-title">Hint</p>
By default, the <code>key</code> is the SHA1 sum of the <code>command + args</code> POSTed to the API. This is done as a rate limiting measure so as to prevent multiple jobs with same parameters, if one such job is already running. If <code>force_unique_key</code> is set to <code>true</code>, the API will bypass this default behaviour and a psuedorandom key will be returned instead.
</div>

<div id="note-post-request" class="admonition note">
<p class="admonition-title">Note</p>
You can see the full JSON schema for the POST request, <a href="https://github.com/Eshaan7/Flask-Shell2HTTP/blob/master/post-request-schema.json" target="_blank">here</a>.
</div>


##### Bonus

You can also define callback functions or use signals for reactive programming. There may be cases where the process doesn't print result to standard output but to a file/database. In such cases, you may want to intercept the future object and update it's result attribute.
I request you to take a look at [Examples.md](Examples.md) for such use-cases.
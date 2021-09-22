# system imports
import logging
import sys

# web imports
from flask import Flask
from flask_executor import Executor
from flask_shell2http import Shell2HTTP

# Flask application instance
app = Flask(__name__)

# Logging
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("flask_shell2http")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# application factory
executor = Executor(app)
shell2http = Shell2HTTP(app, executor, base_url_prefix="/cmd/")

ENDPOINT = "echo"
shell2http.register_command(endpoint=ENDPOINT, command_name=ENDPOINT)


# Test Runner
if __name__ == "__main__":
    app.testing = True
    c = app.test_client()
    """
    The final executed command becomes:
    ```bash
    $ echo hello world
    ```
    """
    # make new request for a command with arguments
    uri = f"/cmd/{ENDPOINT}"
    # timeout in seconds, default value is 3600
    # force_unique_key disables rate-limiting
    data = {"args": ["hello", "world"], "timeout": 60, "force_unique_key": True}
    resp1 = c.post(uri, json=data).get_json()
    print(resp1)
    # fetch result
    result_url = resp1["result_url"].replace("wait=false", "wait=true")
    resp2 = c.get(result_url).get_json()
    print(resp2)

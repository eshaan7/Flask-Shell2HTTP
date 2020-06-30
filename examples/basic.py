# system imports
import requests
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

shell2http.register_command(endpoint=ENDPOINT, command_name="echo")


@app.route("/")
def test():
    """
    The final executed command becomes:
    ```bash
    $ echo hello world
    ```
    """
    url = f"http://localhost:4000/cmd/{ENDPOINT}"
    data = {"args": ["hello", "world"]}
    resp = requests.post(url, json=data)
    resp_data = resp.json()
    print(resp_data)
    key = resp_data["key"]
    if key:
        report = requests.get(f"{url}?key={key}")
        return report.json()
    return resp_data


# Application Runner
if __name__ == "__main__":
    app.run(port=4000)

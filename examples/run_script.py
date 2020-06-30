# system imports
import requests

# web imports
from flask import Flask
from flask_executor import Executor
from flask_shell2http import Shell2HTTP

# Flask application instance
app = Flask(__name__)

# application factory
executor = Executor(app)
shell2http = Shell2HTTP(app, executor, base_url_prefix="/scripts/")

shell2http.register_command(endpoint="hacktheplanet", command_name="./fuxsocy.py")


@app.route("/")
def test():
    """
    The final executed command becomes:
    ```bash
    $ ./fuxsocy.py
    ```
    """
    url = "http://localhost:4000/scripts/hacktheplanet"
    resp = requests.post(url)
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

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


# Application Runner
if __name__ == "__main__":
    app.testing = True
    c = app.test_client()
    """
    The final executed command becomes:
    ```bash
    $ ./fuxsocy.py
    ```
    """
    uri = "/scripts/hacktheplanet"
    resp1 = c.post(uri, json={"args": []}).get_json()
    print(resp1)
    # fetch result
    result_url = resp1["result_url"]
    resp2 = c.get(result_url).get_json()
    print(resp2)

# system imports
import requests
import tempfile
import json

# web imports
from flask import Flask
from flask_executor import Executor
from flask_shell2http import Shell2HTTP

# Flask application instance
app = Flask(__name__)

# application factory
executor = Executor()
executor.init_app(app)
shell2http = Shell2HTTP(base_url_prefix="/cmd/")
shell2http.init_app(app, executor)

shell2http.register_command(endpoint="strings", command_name="strings")


# go to http://localhost:4000/ to execute
@app.route("/")
def test():
    """
    Prefix each filename with @ in arguments.\n
    Files are stored in temporary directories which are flushed on command completion.\n
    The final executed command becomes:
    ```bash
    $ strings /tmp/inputfile /tmp/someotherfile
    ```
    """
    url = "http://localhost:4000/cmd/strings"
    # create and read dummy data from temporary files
    with tempfile.TemporaryFile() as fp:
        fp.write(b"Hello world!")
        fp.seek(0)
        f = fp.read()
    # they key should be `request_json` only.
    form_data = {"args": ["@inputfile", "@someotherfile"]}
    req_data = {"request_json": json.dumps(form_data)}
    req_files = {"inputfile": f, "someotherfile": f}
    resp = requests.post(url=url, files=req_files, data=req_data)
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

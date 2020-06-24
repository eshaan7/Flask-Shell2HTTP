# system imports
import requests
import tempfile

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

ENDPOINT = "catthisformeplease"

shell2http.register_command(endpoint=ENDPOINT, command_name="strings")


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
    url = f"http://localhost:4000/cmd/{ENDPOINT}"
    data = {"args": ["@inputfile", "@someotherfile"]}
    with tempfile.TemporaryFile() as fp:
        fp.write(b"Hello world!")
        fp.seek(0)
        f = fp.read()
        files = {"inputfile": f, "someotherfile": f}
    resp = requests.post(url=url, files=files, data=data)
    resp_data = resp.json()
    print(resp_data)
    key = resp_data["key"]
    if key:
        resp2 = requests.get(f"{url}?key={key}")
        return resp2.json()
    else:
        return resp_data


# Application Runner
if __name__ == "__main__":
    app.run(port=4000)

# web imports
from flask import Flask
from flask_executor import Executor
from flask_executor.futures import Future
from flask_shell2http import Shell2HTTP

# Flask application instance
app = Flask(__name__)

# application factory
executor = Executor(app)
shell2http = Shell2HTTP(app, executor)

ENDPOINT = "echo"


def intercept_result(future: Future):
    """
    Will be invoked on every process completion
    """
    data = None
    if future.done():
        with open("/path/to/saved/file") as f:
            data = f.read()
        # 1. get current result object
        res = future.result()
        # 2. update the report variable,
        # you may update only these: report,error,status
        res.report = data
        res.status = "success"
        # 3. set new result
        future._result = res


shell2http.register_command(
    endpoint=ENDPOINT, command_name=ENDPOINT, callback_fn=intercept_result
)


# Test Runner
if __name__ == "__main__":
    app.testing = True
    c = app.test_client()
    # request new process
    data = {"args": ["hello", "world"]}
    r = c.post(f"/{ENDPOINT}", json=data)
    # get result
    result_url = r.get_json()["result_url"]
    resp = c.get(result_url)
    print(resp.get_json())

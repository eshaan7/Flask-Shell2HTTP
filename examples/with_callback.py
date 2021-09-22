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


def my_callback_fn(extra_callback_context, future: Future):
    """
    Will be invoked on every process completion
    """
    print("[i] Process running ?:", future.running())
    print("[i] Process completed ?:", future.done())
    print("[+] Result: ", future.result())
    # future.result() returns a dictionary
    print("[+] Context: ", extra_callback_context)


shell2http.register_command(
    endpoint="echo/callback", command_name="echo", callback_fn=my_callback_fn
)


# Test Runner
if __name__ == "__main__":
    app.testing = True
    c = app.test_client()
    # request new process
    data = {"args": ["hello", "world"]}
    c.post("/echo/callback", json=data)
    # request another new process
    data = {"args": ["Hello", "Friend!"], "callback_context": {"testkey": "testvalue"}}
    c.post("/echo/callback", json=data)

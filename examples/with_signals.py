# web imports
from flask import Flask
from blinker import Namespace  # or from flask.signals import Namespace
from flask_executor import Executor
from flask_executor.futures import Future
from flask_shell2http import Shell2HTTP

# Flask application instance
app = Flask(__name__)

# application factory
executor = Executor(app)
shell2http = Shell2HTTP(app, executor, base_url_prefix="/cmd/")

ENDPOINT = "echo"
CMD = "echo"

# Signal Handling
signal_handler = Namespace()
my_signal = signal_handler.signal(f"on_{CMD}_complete")
# ..or any other name of your choice,


@my_signal.connect
def my_callback_fn(future: Future):
    """
    Will be invoked on every process completion
    """
    print("Process completed ?:", future.done())
    print("Result: ", future.result())


shell2http.register_command(
    endpoint=ENDPOINT, command_name=CMD, callback_fn=my_signal.send
)


# Test Runner
if __name__ == "__main__":
    app.testing = True
    c = app.test_client()
    # request new process
    data = {"args": ["Hello", "Friend!"]}
    c.post(f"cmd/{ENDPOINT}", json=data)
    # request new process
    data = {"args": ["Bye", "Friend!"]}
    c.post(f"cmd/{ENDPOINT}", json=data)

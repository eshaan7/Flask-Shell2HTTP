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
shell2http = Shell2HTTP(app, executor)

# Signal Handling
signal_handler = Namespace()
my_signal = signal_handler.signal("on_echo_complete")
# ..or any other name of your choice


@my_signal.connect
def my_callback_fn(sender, extra_callback_context, future: Future):
    """
    Will be invoked on every process completion
    """
    print("Process completed ?:", future.done())
    print("Result: ", future.result())


def send_proxy(extra_callback_context, future: Future):
    my_signal.send(
        "send_proxy", extra_callback_context=extra_callback_context, future=future
    )


shell2http.register_command(
    endpoint="echo/signal", command_name="echo", callback_fn=send_proxy
)


# Test Runner
if __name__ == "__main__":
    app.testing = True
    c = app.test_client()
    # request new process
    data = {"args": ["Hello", "Friend!"]}
    c.post("/echo/signal", json=data)
    # request new process
    data = {"args": ["Bye", "Friend!"]}
    c.post("/echo/signal", json=data)

# generic imports
import functools

# web imports
from flask import Flask, request, g, abort, Response
from flask_executor import Executor
from flask_shell2http import Shell2HTTP

# Flask application instance
app = Flask(__name__)

# application factory
executor = Executor(app)
shell2http = Shell2HTTP(app, executor, base_url_prefix="/cmd/")


# few decorators [1]
def logging_decorator(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        print("*" * 64)
        print(
            "from logging_decorator: " + request.url + " : " + str(request.remote_addr)
        )
        print("*" * 64)
        return f(*args, **kwargs)

    return decorator


def login_required(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        if not hasattr(g, "user") or g.user is None:
            abort(Response("You are not logged in.", 401))
        return f(*args, **kwargs)

    return decorator


shell2http.register_command(
    endpoint="public/echo", command_name="echo", decorators=[logging_decorator]
)

shell2http.register_command(
    endpoint="protected/echo",
    command_name="echo",
    decorators=[login_required, logging_decorator],  # [2]
)

# [1] View Decorators:
# https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
# [2] remember that decorators are applied from left to right in a stack manner.
# But are executed in right to left manner.
# Put logging_decorator first and you will see what happens.


# Test Runner
if __name__ == "__main__":
    app.testing = True
    c = app.test_client()
    # request 1
    data = {"args": ["hello", "world"]}
    r1 = c.post("cmd/public/echo", json=data)
    print(r1.json, r1.status_code)
    # request 2
    data = {"args": ["Hello", "Friend!"]}
    r2 = c.post("cmd/protected/echo", json=data)
    print(r2.data, r2.status_code)

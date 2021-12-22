# web imports
from flask import Flask
from flask_executor import Executor
from flask_shell2http import Shell2HTTP

# Flask application instance
app = Flask(__name__)

# application factory
executor = Executor(app)
shell2http = Shell2HTTP(app, executor)


shell2http.register_command(
    endpoint="sleep",
    command_name="sleep",
)


# Test Runner
if __name__ == "__main__":
    app.testing = True
    c = app.test_client()
    # request new process
    r1 = c.post("/sleep", json={"args": ["10"], "force_unique_key": True})
    print(r1)
    # request cancellation
    r2 = c.delete(f"/sleep?key={r1.get_json()['key']}")
    print(r2)

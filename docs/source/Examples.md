## Examples

I have created some example python scripts to demonstrate various use-cases. These include extension setup as well as making test HTTP calls with python's [requests](https://requests.readthedocs.io/en/master/) module.

- [run_script.py](https://github.com/Eshaan7/Flask-Shell2HTTP/blob/master/examples/run_script.py): Execute a script on a succesful POST request to an endpoint.
- [basic.py](https://github.com/Eshaan7/Flask-Shell2HTTP/blob/master/examples/basic.py): Map a base command to an endpoint and pass dynamic arguments to it. Can also pass in a timeout.
- [multiple_files.py](https://github.com/Eshaan7/Flask-Shell2HTTP/blob/master/examples/multiple_files.py): Upload multiple files for a single command.
- [with_callback.py](https://github.com/Eshaan7/Flask-Shell2HTTP/blob/master/examples/with_callback.py): Define a callback function that executes on command/process completion.
- [with_signals.py](https://github.com/Eshaan7/Flask-Shell2HTTP/blob/master/examples/with_signals.py): Using [Flask Signals](https://flask.palletsprojects.com/en/1.1.x/signals/) as callback function.
- [with_decorators.py](https://github.com/Eshaan7/Flask-Shell2HTTP/blob/master/examples/with_decorators.py): Shows how to apply [View Decorators](https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/) to the exposed endpoint. Useful in case you wish to apply authentication, caching, etc. to the endpoint.
- [custom_save_fn.py](https://github.com/Eshaan7/Flask-Shell2HTTP/blob/master/examples/custom_save_fn.py): There may be cases where the process doesn't print result to standard output but to a file/database. This example shows how to pass additional context to the callback function, intercept the future object after completion and update it's result attribute before it's ready to be consumed.
- [deletion.py](https://github.com/Eshaan7/Flask-Shell2HTTP/blob/master/examples/deletion.py): Example demonstrating how to request cancellation/deletion of an already running job.

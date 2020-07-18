## Logging Configuration

This extension logs messages of different severity `INFO`, `DEBUG`, `ERROR` 
using the python's inbuilt [logging](https://docs.python.org/3/library/logging.html) module.

There are no default handlers or stream defined for the logger so it's upto the user to define them.

Here's a snippet of code that shows how you can access this extension's logger object and add a custom handler to it.

```python
# python's inbuilt logging module
import logging
# get the flask_shell2http logger
logger = logging.getLogger("flask_shell2http")
# create new handler
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
# log messages of severity DEBUG or lower to the console
logger.setLevel(logging.DEBUG)  # this is really important!
```

Please consult the Flask's official docs on 
[extension logs](https://flask.palletsprojects.com/en/1.1.x/logging/#other-libraries) for more details.
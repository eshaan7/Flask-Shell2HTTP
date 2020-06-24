# system imports
from collections import OrderedDict

# lib imports
from .api import shell2httpAPI


class Shell2HTTP(object):
    """
    Flask-Shell2HTTP base entrypoint class. The only public API available to users.
    Example:
    ----------
    ```python
    app = Flask(__name__)
    executor = Executor(app)
    shell2http = Shell2HTTP(app=app, executor=executor, base_url_prefix="/tasks/")
    ```
    """

    __commands: "OrderedDict[str, str]" = OrderedDict()
    __url_prefix: str = "/"

    def __init__(self, app=None, executor=None, base_url_prefix="/") -> None:
        self.__url_prefix = base_url_prefix
        if app and executor:
            self.init_app(app, executor)

    def init_app(self, app, executor) -> None:
        """
        For use with Flask's
        [Application Factory]
        (https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/)
        method.
        Example:
        ----------
        ```python
        executor = Executor()
        shell2http = Shell2HTTP(base_url_prefix="/commands/")
        app = Flask(__name__)
        executor.init_app(app)
        shell2http.init_app(app=app, executor=executor)
        ```
        """
        self.app = app
        self.__executor = executor
        self.__init_extension()

    def __init_extension(self) -> None:
        """
        For internal use only.
        adds the Shell2HTTP() instance to `Flask().extensions` list
        """
        if not hasattr(self.app, "extensions"):
            self.app.extensions = dict()

        self.app.extensions["shell2http"] = self

    def register_command(self, endpoint: str, command_name: str) -> None:
        """
        :param endpoint: string
            your command would live here: `/{base_url_prefix}/{endpoint}`
        :param command_name: string
            - The base command which can be executed from this endpoint.
            - If you pass in `echo`, then all commands given
              to this endpoint MUST start with `echo`.
              For example, `["echo", "hello", "world"]`.
            - This is more of a security mechanism than functionality.
        Example:
        ----------
        ```python
        shell2http.register_command(endpoint="echo", command_name="echo")
        shell2http.register_command(
            endpoint="myawesomescript", command_name="./fuxsocy.py"
        )
        ```
        """
        url = self.__construct_route(endpoint)
        self.app.add_url_rule(
            url,
            view_func=shell2httpAPI.as_view(
                command_name, command_name=command_name, executor=self.__executor
            ),
        )
        self.__commands.update({command_name: url})

    def get_registered_commands(self):
        """
        :returns:
            OrderedDict of registered commands and their urls.
        """
        return self.__commands

    def __construct_route(self, endpoint: str) -> str:
        """
        For internal use only.
        """
        return self.__url_prefix + endpoint

# system imports
from collections import OrderedDict
from typing import Callable, Dict, List, Any

# web imports
from flask import Blueprint
from flask_executor import Executor
from flask_executor.futures import Future

# lib imports
from .api import Shell2HttpAPI
from .helpers import get_logger


logger = get_logger()


class Shell2HTTP(Blueprint):
    """
    Flask-Shell2HTTP's base entrypoint. This is the only public API available to users.

    This is a subclass of `Flask.Blueprint` so it accepts
    all the same arguments and functionality of a generic ``Flask.Blueprint`` instance..

    Attributes:
        executor: ``flask_executor.Executor`` instance
        import_name: The name of the blueprint package, usually
            ``__name__``. This helps locate the ``root_path`` for the
            blueprint.
        static_folder: A folder with static files that should be
            served by the blueprint's static route. The path is relative to
            the blueprint's root path. Blueprint static files are disabled
            by default.
        static_url_path: The url to serve static files from.
            Defaults to ``static_folder``. If the blueprint does not have
            a ``url_prefix``, the app's static route will take precedence,
            and the blueprint's static files won't be accessible.
        template_folder: A folder with templates that should be added
            to the app's template search path. The path is relative to the
            blueprint's root path. Blueprint templates are disabled by
            default. Blueprint templates have a lower precedence than those
            in the app's templates folder.
        url_prefix: A path to prepend to all of the blueprint's URLs,
            to make them distinct from the rest of the app's routes.
        subdomain: A subdomain that blueprint routes will match on by
            default.
        url_defaults: A dict of default values that blueprint routes
            will receive by default.
        root_path: By default, the blueprint will automatically this
            based on ``import_name``. In certain situations this automatic
            detection can fail, so the path can be specified manually
            instead.

    Example::

        app = Flask(__name__)
        executor = Executor(app)
        shell2http = Shell2HTTP(executor, 'tasks', __name__, url_prefix="/tasks")
    """

    __commands: "OrderedDict[str, str]"
    __executor: Executor

    def __init__(self, executor: Executor, *args, **kwargs):
        self.__commands = OrderedDict()
        self.__executor = executor
        super().__init__(*args, **kwargs)

    def register_command(
        self,
        endpoint: str,
        command_name: str,
        callback_fn: Callable[[Dict, Future], Any] = None,
        decorators: List = [],
    ) -> None:
        """
        Function to map a shell command to an endpoint or route.

        This internally registers the route via the ``Blueprint.add_url_rule`` method
        so you can enjoy all the same features and powers of a blueprint instance.

        Args:
            endpoint (str):
                - your command would live here: ``/{url_prefix}/{endpoint}``
            command_name (str):
                - The base command which can be executed from the given endpoint.
                - If ``command_name='echo'``, then all arguments passed
                  to this endpoint will be appended to ``echo``.\n
                  For example,
                  if you pass ``{ "args": ["Hello", "World"] }``
                  in POST request, it gets converted to ``echo Hello World``.\n
            callback_fn (Callable[[Dict, Future], Any]):
                - An optional function that is invoked when a requested process
                    to this endpoint completes execution.
                - This is added as a
                    ``concurrent.Future.add_done_callback(fn=callback_fn)``
                - The same callback function may be used for multiple commands.
                - if request JSON contains a `callback_context` attr, it will be passed
                  as the first argument to this function.
            decorators (List[Callable]):
                - A List of view decorators to apply to the endpoint.
                - *New in version v1.5.0*

        Examples::

            def my_callback_fn(context: dict, future: Future) -> None:
                print(future.result(), context)

            shell2http.register_command(endpoint="echo", command_name="echo")
            shell2http.register_command(
                endpoint="myawesomescript",
                command_name="./fuxsocy.py",
                callback_fn=my_callback_fn,
                decorators=[],
            )
        """
        # make sure the given endpoint is not already registered
        cmd_already_exists = self.__commands.get(endpoint)
        if cmd_already_exists:
            err_msg = (
                "Failed to register since given endpoint: "
                f"'{endpoint}' already maps to command: '{cmd_already_exists}'."
            )
            logger.error(err_msg)
            raise AssertionError(err_msg)

        # else, add new URL rule
        view_func = Shell2HttpAPI.as_view(
            endpoint,
            command_name=command_name,
            user_callback_fn=callback_fn,
            executor=self.__executor,
        )
        # apply decorators, if any
        for dec in decorators:
            view_func = dec(view_func)
        # register URL rule
        self.add_url_rule(
            endpoint,
            view_func=view_func,
        )
        self.__commands.update({endpoint: command_name})
        logger.info(
            f"New endpoint: '{self.url_prefix}/{endpoint}' "
            f"registered for command: '{command_name}'."
        )

    def get_registered_commands(self) -> "OrderedDict[str, str]":
        """
        Most of the time you won't need this since
        Flask provides a ``Flask.url_map`` attribute.

        Returns:
            OrderedDict[uri, command]
            i.e. mapping of registered commands and their URLs.
        """
        return self.__commands

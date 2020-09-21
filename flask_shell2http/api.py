"""
    flask_shell2http.api
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Flask-Shell2HTTP API class
    :copyright: (c) 2020 by Eshaan Bansal.
    :license: BSD, see LICENSE for more details.
"""

# system imports
import functools
from http import HTTPStatus
from typing import Callable, Dict, Any

# web imports
from flask import request, jsonify, make_response
from flask.views import MethodView
from flask_executor import Executor
from flask_executor.futures import Future

# lib imports
from .classes import RequestParser, run_command
from .helpers import get_logger


logger = get_logger()
request_parser = RequestParser()


class shell2httpAPI(MethodView):
    """
    Flask.MethodView that registers GET and POST methods for a given endpoint.
    This is invoked on `Shell2HTTP.register_command`.
    Internal use only.
    """

    def get(self):
        try:
            key: str = request.args.get("key")
            logger.info(
                f"Job: '{key}' --> Report requested. "
                f"Requester: '{request.remote_addr}'."
            )
            if not key:
                raise Exception("No key provided in arguments.")

            # get the future object
            future: Future = self.executor.futures._futures.get(key)
            if not future:
                raise Exception(f"No report exists for key: '{key}'.")

            # check if job has been finished
            if not future.done():
                logger.debug(f"Job: '{key}' --> still running.")
                return make_response(jsonify(status="running", key=key), 200)

            # pop future object since it has been finished
            self.executor.futures.pop(key)

            # if yes, get result from store
            report: Dict = future.result()
            if not report:
                raise Exception(f"Job: '{key}' --> No report exists.")

            logger.debug(f"Job: '{key}' --> Requested report: {report}")
            return jsonify(report)

        except Exception as e:
            logger.error(e)
            return make_response(jsonify(error=str(e)), HTTPStatus.NOT_FOUND)

    def post(self):
        try:
            logger.info(
                f"Received request for endpoint: '{request.url_rule}'. "
                f"Requester: '{request.remote_addr}'."
            )
            # Check if request data is correct and parse it
            cmd, timeout, callback_context, key = request_parser.parse_req(
                request, self.command_name
            )

            # run executor job in background
            future = self.executor.submit_stored(
                future_key=key, fn=run_command, cmd=cmd, timeout=timeout, key=key,
            )
            # callback that removes the temporary directory
            future.add_done_callback(request_parser.cleanup_temp_dir)
            if self.user_callback_fn:
                # user defined callback fn with callback_context if any
                future.add_done_callback(
                    functools.partial(self.user_callback_fn, callback_context)
                )

            logger.info(f"Job: '{key}' --> added to queue for command: {cmd}")
            result_url = f"{request.base_url}?key={key}"
            return make_response(
                jsonify(status="running", key=key, result_url=result_url),
                HTTPStatus.ACCEPTED,
            )

        except Exception as e:
            logger.error(e)
            return make_response(jsonify(error=str(e)), HTTPStatus.BAD_REQUEST)

    def __init__(
        self,
        command_name: str,
        user_callback_fn: Callable[[Dict, Future], Any],
        executor: Executor,
    ):
        self.command_name: str = command_name
        self.user_callback_fn = user_callback_fn
        self.executor: Executor = executor

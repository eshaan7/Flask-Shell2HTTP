"""
    flask_shell2http.api
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Flask-Shell2HTTP API class
    :copyright: (c) 2020 by Eshaan Bansal.
    :license: BSD, see LICENSE for more details.
"""

# system imports
from http import HTTPStatus

# web imports
from flask import request, jsonify, make_response
from flask.views import MethodView

# lib imports
from .classes import JobExecutor, ReportStore, RequestParser
from .helpers import get_logger


logger = get_logger()
store = ReportStore()
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
            # check if job has been finished
            future = self.executor.get_job(key)
            if future:
                if not future.done:
                    logger.debug(f"Job: '{key}' --> still running.")
                    return make_response(jsonify(status="running", key=key), 200)

                # pop future object since it has been finished
                self.executor.pop_job(key)

            # if yes, get result from store
            report = store.pop_and_get_one(key)
            if not report:
                raise Exception(f"No report exists for key: '{key}'.")

            resp = report.to_dict()
            logger.debug(f"Job: '{key}' --> Requested report: {resp}")
            return make_response(jsonify(resp), HTTPStatus.OK)

        except Exception as e:
            logger.error(e)
            return make_response(jsonify(error=str(e)), HTTPStatus.NOT_FOUND)

    def post(self):
        try:
            logger.info(
                f"Received request for endpoint: '{request.url_rule}'. "
                f"Requester: '{request.remote_addr}'."
            )
            # Check if command is correct and parse it
            cmd, key = request_parser.parse_req(request, self.command_name)

            # run executor job in background
            future = self.executor.new_job(
                future_key=JobExecutor.make_key(key),
                fn=self.executor.run_command,
                cmd=cmd,
                key=key,
            )
            # callback that adds result to store
            future.add_done_callback(store.save_result)
            # callback that removes the temporary directory
            future.add_done_callback(request_parser.cleanup_temp_dir)

            logger.info(f"Job: '{key}' --> added to queue for command: {cmd}")
            result_url = f"{request.base_url}?key={key}"
            return make_response(
                jsonify(status="running", key=key, result_url=result_url),
                HTTPStatus.ACCEPTED,
            )

        except Exception as e:
            logger.error(e)
            return make_response(jsonify(error=str(e)), HTTPStatus.BAD_REQUEST)

    def __init__(self, command_name, job_executor):
        self.command_name: str = command_name
        self.executor: JobExecutor = job_executor

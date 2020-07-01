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


class shell2httpAPI(MethodView):
    """
    Flask.MethodView that defines GET and POST methods for an URL rule.
    This is invoked on `Shell2HTTP.register_command`, in which case
    the URL rule is the given endpoint.
    Internal use only.
    """

    command_name: str
    executor: JobExecutor
    store: ReportStore
    request_parser: RequestParser

    def get(self):
        try:
            key: str = request.args.get("key")
            logger.info(f"Report requested for key:'{key}'.")
            if not key:
                raise Exception("No key provided in arguments.")
            # check if job has been finished
            future = self.executor.get_job(key)
            if future:
                if not future.done:
                    return make_response(jsonify(status="running", key=key), 200)

                # pop future object since it has been finished
                self.executor.pop_job(key)

            # if yes, get result from store
            report = self.store.get_one(key)
            if not report:
                raise Exception(f"Report does not exist for key:{key}.")

            resp = report.to_dict()
            logger.debug(f"Requested report: {resp}")
            return make_response(jsonify(resp), HTTPStatus.OK)

        except Exception as e:
            logger.exception(e)
            return make_response(jsonify(error=str(e)), HTTPStatus.NOT_FOUND)

    def post(self):
        try:
            logger.info(f"Received request for endpoint: '{request.url_rule}'.")
            # Check if command is correct and parse it
            cmd, key = self.request_parser.parse_req(request)

            # run executor job in background
            job_key = JobExecutor.make_key(key)
            future = self.executor.new_job(
                future_key=job_key, fn=self.executor.run_command, cmd=cmd, key=key
            )
            # callback that adds result to store
            future.add_done_callback(self.store.save_result)
            # callback that removes the temporary directory
            future.add_done_callback(self.request_parser.cleanup_temp_dir)

            logger.info(f"Job: '{job_key}' added to queue for command: {cmd}")
            return make_response(
                jsonify(status="running", key=key), HTTPStatus.ACCEPTED,
            )

        except Exception as e:
            logger.exception(e)
            return make_response(jsonify(error=str(e)), HTTPStatus.BAD_REQUEST)

    def __init__(self, command_name, executor):
        self.command_name = command_name
        self.executor = JobExecutor(executor)
        self.store = ReportStore()
        self.request_parser = RequestParser(command_name)

# system imports
import time
import subprocess
import tempfile
import shutil
from collections import OrderedDict
from typing import List, Dict

# web imports
from flask import safe_join
from werkzeug.utils import secure_filename
from http import HTTPStatus
from flask_executor import Executor

# lib imports
from .helpers import list_replace, calc_hash, get_logger

logger = get_logger()


class Report:
    """
    Report class to store the command's result.
    Internal use only.
    """

    def __init__(self, key, report, error, start_time, status="failed"):
        self.start_time = start_time
        self.end_time = time.time()
        self.process_time = self.end_time - self.start_time
        self.key = key
        self.report = report
        self.error = error
        self.status = status

    def to_dict(self):
        resp = self.__dict__
        return resp


class JobExecutor:
    """
    A high-level API for flask_executor.Executor() to allow common operations.
    Internal use only.
    """

    executor: Executor

    @staticmethod
    def make_key(k) -> str:
        return f"job_{k}"

    def get_job(self, k):
        key = self.make_key(k)
        return self.executor.futures._futures.get(key, None)

    def cancel_job(self, k):
        key = self.make_key(k)
        return self.executor.futures._futures.get(key).cancel()

    def new_job(self, **kwargs):
        return self.executor.submit_stored(**kwargs)

    def pop_job(self, k):
        key = self.make_key(k)
        return self.executor.futures.pop(key)

    def __init__(self, executor) -> None:
        self.executor = executor

    def run_command(self, cmd, key) -> Report:
        """
        This function is called by the executor to run given command
        using a subprocess asynchronously.

        :returns:
            A ConcurrentFuture object where future.result = Report()
        """
        start_time = time.time()
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            stdout = stdout.decode("ascii")
            stderr = stderr.decode("ascii")
            if stderr and stdout:
                status = "reported_with_fails"
            elif stdout and not stderr:
                status = "success"
            else:
                status = "failed"

            logger.info(f"Job: '{key}' --> finished with status: '{status}'.")
            return Report(
                key=key,
                report=stdout,
                error=stderr,
                start_time=start_time,
                status=status,
            )

        except Exception as e:
            str_err = str(e)
            self.cancel_job(key)
            logger.error(f"Job: '{key}' --> failed. Reason: {str_err}.")
            return Report(
                key=key,
                report=None,
                error=str_err,
                start_time=start_time,
                status="failed",
            )


class ReportStore:
    """
    Acts as a data-store for command's results.
    """

    __results: "OrderedDict[str, Report]" = OrderedDict()

    def save_result(self, future) -> None:
        """
        callback fn for Future object.
        """
        # get job result from future
        job_res = future.result()
        self.__results.update({job_res.key: job_res})

    def get_all(self):
        return self.__results

    def pop_and_get_one(self, key) -> Report:
        try:
            return self.__results.pop(key)
        except KeyError:
            return None


class RequestParser:
    """
    Utility class to parse incoming POST request data into meaningful arguments.
    Internal use Only.
    """

    __tmpdirs: Dict[str, str] = {}

    @staticmethod
    def __parse_multipart_req(args: List[str], files) -> (List[str], str):
        # Check if file part exists
        fnames = []
        for arg in args:
            if arg.startswith("@"):
                fnames.append(arg.strip("@"))

        if not fnames:
            raise Exception(
                "No filename(s) specified."
                "Please prefix file argument(s) with @ character.",
                HTTPStatus.BAD_REQUEST,
            )

        # create a new temporary directory
        tmpdir: str = tempfile.mkdtemp()
        for fname in fnames:
            if fname not in files:
                raise Exception(
                    f"No File part with filename: {fname} in request.",
                    HTTPStatus.BAD_REQUEST,
                )
            req_file = files.get(fname)
            filename = secure_filename(req_file.filename)
            # calc file location
            f_loc = safe_join(tmpdir, filename)
            # save file into temp directory
            req_file.save(f_loc)
            # replace @filename with it's file location in system
            list_replace(args, "@" + fname, f_loc)

        logger.debug(f"Request files saved under temp directory: '{tmpdir}'")
        return args, tmpdir

    def parse_req(self, request, base_command: str) -> (str, str):
        args: List[str] = []
        tmpdir = None
        if request.is_json:
            # request does not contain a file
            args = request.json.get("args", [])
        elif request.files:
            # request contains file
            received_args = request.form.getlist("args")
            args, tmpdir = RequestParser.__parse_multipart_req(
                received_args, request.files
            )
        else:
            # request is w/o any data
            # i.e. just run-script
            args = []

        cmd: List[str] = base_command.split(" ")
        cmd.extend(args)
        key: str = calc_hash(cmd)
        if tmpdir:
            self.__tmpdirs.update({key: tmpdir})

        return cmd, key

    def cleanup_temp_dir(self, future) -> None:
        key: str = future.result().key
        tmpdir: str = self.__tmpdirs.get(key, None)
        if not tmpdir:
            return None

        try:
            shutil.rmtree(tmpdir)
            logger.debug(
                f"Job: '{key}' --> Temporary directory: '{tmpdir}' "
                "successfully deleted."
            )
            self.__tmpdirs.pop(key)
        except Exception:
            logger.debug(
                f"Job: '{key}' --> Failed to clear Temporary directory: '{tmpdir}'."
            )

# system imports
import time
import subprocess
import tempfile
from collections import OrderedDict

# web imports
from werkzeug.utils import secure_filename
from http import HTTPStatus
from flask_executor import Executor

# lib imports
from .helpers import list_replace, calc_hash


class Report:
    """
    Report class to store the command's result.
    Internal use only.
    """
    def __init__(self, md5, report, error, start_time, status="failed"):
        self.start_time = start_time
        self.end_time = time.time()
        self.process_time = self.end_time - self.start_time
        self.md5 = md5
        self.report = report
        self.error = error
        self.status = status

    def to_json(self):
        resp = self.__dict__
        # resp["report"] = json.loads(self.report)
        return resp


class JobExecutor:
    """
    A high-level API for flask_executor.Executor() to allow common operations.
    Internal use only.
    """
    executor: Executor

    @staticmethod
    def make_key(md5) -> str:
        return f"job_{md5}"

    def get_job(self, md5):
        key = self.make_key(md5)
        return self.executor.futures._futures.get(key, None)

    def cancel_job(self, md5):
        key = self.make_key(md5)
        return self.executor.futures._futures.get(key).cancel()

    def new_job(self, **kwargs):
        return self.executor.submit_stored(**kwargs)

    def pop_job(self, md5):
        key = self.make_key(md5)
        return self.executor.futures.pop(key)

    def __init__(self, executor) -> None:
        self.executor = executor

    def run_command(self, cmd, md5) -> Report:
        """
        This function is called by the executor to run given command
        using a subprocess asynchronously.

        :returns:
            A ConcurrentFuture object where future.result = Report()
        """
        try:
            start_time = time.time()
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

            stdout = {"result": stdout}
            return Report(
                md5=md5,
                report=stdout,
                error=stderr,
                start_time=start_time,
                status=status,
            )

        except Exception as e:
            self.cancel_job(md5)
            return Report(
                md5=md5,
                report=None,
                error=str(e),
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
        self.__results.update({job_res.md5: job_res})

    def get_all(self):
        return self.__results

    def get_one(self, key) -> Report:
        return self.__results.get(key)


class RequestParser:
    """
    Utility class to parse incoming POST request data into meaningful arguments.
    Internal use Only.
    """
    @staticmethod
    def __parse_multipart_req(args: list, files):
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
        tmpdir = tempfile.mkdtemp()
        for fname in fnames:
            if fname not in files:
                raise Exception(
                    f"No File part with filename: {fname} in request.",
                    HTTPStatus.BAD_REQUEST,
                )
            req_file = files.get(fname)
            filename = secure_filename(req_file.filename)
            # calc file location
            f_loc = __import__("os").path.join(tmpdir, filename)
            # save file into temp directory
            req_file.save(f_loc)
            # replace @filename with it's file location in system
            list_replace(args, "@" + fname, f_loc)

        return args, tmpdir

    def parse_req(self, request):
        if request.is_json:
            # request does not contain a file
            args = request.json.get("args", [])
        elif request.files:
            # request contains file
            received_args = request.form.getlist("args")
            args, self.tmpdir = RequestParser.__parse_multipart_req(
                received_args, request.files
            )
        else:
            # request is w/o any data
            # i.e. just run-script
            args = []

        args.insert(0, self.command_name)
        return args, calc_hash(args)

    def cleanup_temp_dir(self, _):
        if hasattr(self, "tmpdir"):
            __import__("shutil").rmtree(self.tmpdir)

    def __init__(self, command_name):
        self.command_name = command_name

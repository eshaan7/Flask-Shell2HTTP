# system imports
import time
import subprocess
import tempfile
import shutil
import dataclasses
from typing import List, Dict, Any

# web imports
from flask.helpers import safe_join
from werkzeug.utils import secure_filename
from http import HTTPStatus
from flask_executor.futures import Future

# lib imports
from .helpers import list_replace, calc_hash, get_logger, DEFAULT_TIMEOUT

logger = get_logger()


@dataclasses.dataclass
class Report:
    """
    Report dataclass to store the command's result.
    Internal use only.
    """

    key: str
    report: Any
    error: Any
    status: str
    start_time: float
    end_time: float
    returncode: int
    process_time: float = dataclasses.field(init=False)

    def __post_init__(self):
        self.process_time = self.end_time - self.start_time

    def to_dict(self):
        return dataclasses.asdict(self)


def run_command(cmd: List[str], timeout: int, key: str) -> Report:
    """
    This function is called by the executor to run given command
    using a subprocess asynchronously.

    :param cmd: List[str]
        command to run split as a list
    :param key: str
        future_key of particular Future instance
    :param timeout: int
        maximum timeout in seconds (default = 3600)

    :rtype Report

    :returns:
        A Concurrent.Future object where future.result() is the report
    """
    start_time: float = time.time()
    status: str = "failed"
    try:
        p = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text="ascii",
            timeout=timeout,
        )
        stdout, stderr, returncode = p.stdout, p.stderr, p.returncode
        if returncode == 0:
            status = "success"
        elif stderr and stdout:
            status = "reported_with_fails"
        elif stdout and not stderr:
            status = "success"

        logger.info(f"Job: '{key}' --> finished with status: '{status}'.")

    except Exception as e:
        status = "failed"
        returncode = -1
        stdout = None
        stderr = str(e)
        logger.error(f"Job: '{key}' --> failed. Reason: \"{stderr}\".")

    return Report(
        key=key,
        report=stdout,
        error=stderr,
        status=status,
        start_time=start_time,
        end_time=time.time(),
        returncode=returncode,
    )


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
            timeout: int = request.json.get("timeout", DEFAULT_TIMEOUT)
        elif request.files:
            # request contains file
            received_args = request.form.getlist("args")
            timeout: int = request.form.get("timeout", DEFAULT_TIMEOUT)
            args, tmpdir = RequestParser.__parse_multipart_req(
                received_args, request.files
            )
        else:
            # request is w/o any data
            # i.e. just run-script
            args = []
            timeout: int = DEFAULT_TIMEOUT

        cmd: List[str] = base_command.split(" ")
        cmd.extend(args)
        key: str = calc_hash(cmd)
        if tmpdir:
            self.__tmpdirs.update({key: tmpdir})

        return cmd, timeout, key

    def cleanup_temp_dir(self, future: Future) -> None:
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

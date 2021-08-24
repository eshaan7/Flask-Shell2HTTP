# system imports
import time
import json
import subprocess
import tempfile
import shutil
from typing import List, Dict, Tuple, Any, Optional

# web imports
from flask.helpers import safe_join
from werkzeug.utils import secure_filename
from flask_executor.futures import Future

# lib imports
from .helpers import list_replace, gen_key, get_logger, DEFAULT_TIMEOUT

logger = get_logger()


class RunnerParser:
    """
    Utility class to parse incoming POST request
    data into meaningful arguments, generate key and run command.
    Internal use Only.
    """

    __tmpdirs: Dict[str, str] = {}

    @staticmethod
    def __parse_multipart_req(args: List[str], files) -> Tuple[List[str], str]:
        # Check if file part exists
        fnames = []
        for arg in args:
            if arg.startswith("@"):
                fnames.append(arg.strip("@"))

        if not fnames:
            raise Exception(
                "No filename(s) specified."
                "Please prefix file argument(s) with @ character."
            )

        # create a new temporary directory
        tmpdir: str = tempfile.mkdtemp()
        for fname in fnames:
            if fname not in files:
                raise Exception(f"No File part with filename: {fname} in request.")
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

    def parse_req(
        self, request, base_command: str
    ) -> Tuple[List[str], int, Dict[str, Any], str]:
        # default values if request is w/o any data
        # i.e. just run-script
        tmpdir = None
        # default values
        args: List[str] = []
        timeout: int = DEFAULT_TIMEOUT
        callback_context: Dict[str, Any] = {}
        randomize_key = False
        if request.is_json:
            # request does not contain a file
            args = request.json.get("args", [])
            timeout = request.json.get("timeout", DEFAULT_TIMEOUT)
            callback_context = request.json.get("callback_context", {})
            randomize_key = request.json.get("force_unique_key", False)
        elif request.files:
            # request contains file and form_data
            data = json.loads(request.form.get("request_json", "{}"))
            received_args = data.get("args", [])
            timeout = data.get("timeout", DEFAULT_TIMEOUT)
            callback_context = data.get("callback_context", {})
            randomize_key = data.get("force_unique_key", False)
            args, tmpdir = self.__parse_multipart_req(received_args, request.files)

        cmd: List[str] = base_command.split(" ")
        cmd.extend(args)
        key: str = gen_key(cmd, randomize=randomize_key)
        if tmpdir:
            self.__tmpdirs.update({key: tmpdir})

        return cmd, timeout, callback_context, key

    def cleanup_temp_dir(self, future: Future) -> None:
        key: Optional[str] = future.result().get("key", None)
        if not key:
            return None
        tmpdir: Optional[str] = self.__tmpdirs.get(key, None)
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

    @staticmethod
    def run_command(cmd: List[str], timeout: int, key: str) -> Dict[str, Any]:
        """
        This function is called by the executor to run given command
        using a subprocess asynchronously.

        :param cmd: List[str]
            command to run split as a list
        :param key: str
            future_key of particular Future instance
        :param timeout: int
            maximum timeout in seconds (default = 3600)

        :rtype: Dict[str, Any]

        :returns:
            A Concurrent.Future object where future.result() is the report
        """
        start_time: float = time.time()
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout: Optional[str] = None
        stderr: Optional[str] = None
        returncode: int = 0
        try:
            outs, errs = proc.communicate(timeout=int(timeout))
            stdout = outs.decode("utf-8")
            stderr = errs.decode("utf-8")
            returncode = proc.returncode
            logger.info(f"Job: '{key}' --> finished with returncode: '{returncode}'.")

        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, _ = [s.decode("utf-8") for s in proc.communicate()]
            stderr = f"command timedout after {timeout} seconds."
            returncode = proc.returncode
            logger.error(f"Job: '{key}' --> failed. Reason: \"{stderr}\".")

        except Exception as e:
            proc.kill()
            returncode = -1
            stdout = None
            stderr = str(e)
            logger.error(f"Job: '{key}' --> failed. Reason: \"{stderr}\".")

        end_time: float = time.time()
        process_time = end_time - start_time
        return dict(
            key=key,
            report=stdout,
            error=stderr,
            returncode=returncode,
            start_time=start_time,
            end_time=end_time,
            process_time=process_time,
        )

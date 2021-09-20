class JobNotFoundException(Exception):
    """
    Raised when no job exists for requested key.
    """


class JobStillRunningException(Exception):
    """
    Raised when job is still running.
    """

import logging
from typing import List


def list_replace(lst: List, old, new) -> None:
    """
    replace list elements (inplace)
    """
    idx = -1
    try:
        while True:
            i = lst.index(old, idx + 1)
            lst[i] = new
    except ValueError:
        pass


def calc_hash(lst: List) -> str:
    """
    Internal use only.
    Calculates sha1sum of given command with it's byte-string.
    This is for non-cryptographic purpose,
    that's why a faster and insecure hashing algorithm is chosen.
    """
    to_hash = " ".join(lst).encode("ascii")
    return __import__("hashlib").sha1(to_hash).hexdigest()[:12]


def get_logger() -> logging.Logger:
    return logging.getLogger("flask_shell2http")

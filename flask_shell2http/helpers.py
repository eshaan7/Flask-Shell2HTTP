import logging
import hashlib
import uuid
from typing import List

from flask import current_app

DEFAULT_TIMEOUT = 3600


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


def gen_key(lst: List, randomize=False) -> str:
    if randomize:
        return str(uuid.uuid4())[:8]
    return calc_hash(lst)[:8]


def calc_hash(lst: List) -> str:
    """
    Internal use only.
    Calculates sha1sum of given command with it's byte-string.
    This is for non-cryptographic purpose,
    that's why a faster and insecure hashing algorithm is chosen.
    """
    current_app.config.get("Shell2HTTP_")
    to_hash = " ".join(lst).encode("utf-8")
    return hashlib.sha1(to_hash).hexdigest()


def get_logger() -> logging.Logger:
    return logging.getLogger("flask_shell2http")

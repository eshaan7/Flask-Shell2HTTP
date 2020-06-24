def list_replace(lst: list, old, new) -> None:
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


def calc_hash(lst: list) -> str:
    """
    Internal use only.
    Calculates md5sum of given command with it's byte-string.
    """
    to_hash = " ".join(lst).encode("ascii")
    return __import__("hashlib").md5(to_hash).hexdigest()

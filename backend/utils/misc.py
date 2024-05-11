import random
import string
from pathlib import Path
from time import time


def generate_random_string(length):
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=length)  # NOQA: S311
    )


HEALTHCHECK_STATUS_FILE_PATH = Path("/tmp/_healthcheck_status")  # NOQA: S108


def refresh_healthcheck_timestamp() -> None:
    """Updates timestamp used for Celerybeat healthcheck."""
    try:
        with Path.open(HEALTHCHECK_STATUS_FILE_PATH, "w") as status_file:
            status_file.write(f"{str(int(time()))}\n")
    except IOError:
        pass

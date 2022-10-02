import io
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from cat_file.logging import logger as __logger


logger = __logger.getChild(__name__)


def load_file_stream(path: Optional[str] = None) -> io.BytesIO:
    """
    Loads the correct data to a `io.BytesIO` object.
    Args:
        path: If `path` is `None`, then the data is read from the `stdin`; otherwise,
            it is read from the provided `path`
    Returns:
        A `io.BytesIO` object with the data
    """
    if path is None:
        logger.info("Reading STDIN to bytes buffer")
        return io.BytesIO(sys.stdin.buffer.read())
    logger.info("Loading path into bytes buffer")
    return io.BytesIO(Path(path).read_bytes())


@contextmanager
def zero_buffer(buffer: io.IOBase) -> io.IOBase:
    """
    A context manager to reset the buffer pointer before/after
    the usage of the buffer.

    Example:
    >>> import io
    >>> s = io.BytesIO(...)
    >>> s.tell
    0
    >>> with zero_buffer(s) as buffer:
    >>>     buffer.read(10)
    >>>     buffer.tell()
    10
    >>> s.tell()
    0

    Args:
        buffer: A `io.BytesIO` object
    """
    if is_seekable := buffer.seekable():
        buffer.seek(0)

    try:
        yield buffer

    finally:
        if is_seekable:
            buffer.seek(0)

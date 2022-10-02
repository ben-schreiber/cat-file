import argparse
import io
import sys
from collections.abc import Iterable
from functools import lru_cache
from typing import Any
from typing import Union

from .logging import logger as __logger


logger = __logger.getChild(__name__)


def staticclass(cls: Any) -> Any:
    """
    A function to be used as a wrapper for a class.
    Will convert the class to a static class which
    will not need to be instantiated.

    Example:
    >>> @staticclass
    >>> class Foo:
    >>>     def goo(self, a):
    >>>         print(a)
    >>>
    >>> Foo.goo('Hello World')
    Hello World
    >>>
    >>> Foo()
    ...
    TypeError: 'Foo' object is not callable
    """
    return cls()


@lru_cache
def should_read_from_stdin() -> bool:
    """
    Returns boolean flag if there is data being piped in to the program from STDIN

    Returns:
        `True` if data is being piped in from STDIN, else `False`
    """
    should_read = not sys.stdin.isatty()
    logger.debug(f'Reading from {"stdin pipe" if should_read else "provided path"}')
    return should_read


def get_num_lines_to_print(args: argparse.Namespace) -> Union[int, None]:
    """
    Given the `argparse.Namespace` object, returns the number of lines
    to print.

    Args:
        args: A `argparse.Namespace` object

    Returns:
        If `head` was passed as a CLI parameter, then the result
        will be positive. If `tail` was passed as a CLI parameter then the
        result will be negative. `None` is returned when nothing was
        passed to the CLI
    """
    if args.head is not None:
        logger.debug(f"Received {args.head=}")
        return args.head

    if args.tail is not None:
        logger.debug(f"Received {args.tail=}")
        return args.tail if args.tail < 0 else -args.tail


def get_path_from_args(args: argparse.Namespace) -> Union[str, None]:
    if not should_read_from_stdin():
        return args.path[0] if isinstance(args.path, Iterable) else args.path

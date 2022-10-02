from __future__ import annotations

from typing import Callable
from typing import Iterator
from typing import Tuple
from typing import TYPE_CHECKING
from typing import TypeVar

from cat_file.errors import DuplicateFileTypeCodeError
from cat_file.errors import InvalidFileTypeError
from cat_file.logging import logger as _l
from cat_file.utils import staticclass


if TYPE_CHECKING:
    from filetypes._base import DataFile


logger = _l.getChild(__name__)
_C = TypeVar("_C")


@staticclass
class filetype:
    """
    A singleton manager class for all file types.

    How to register a class with the manager
    >>> @filetype.register(code='a')
    >>> class AFileType:
    >>>     ...

    This class is `Iterable`, so iterating over the
    class returns tuples of the code and class object
    """

    def __init__(self) -> None:
        self._types = {}

    def register(self, *, code: str) -> Callable[[_C], _C]:
        def inner(cls: _C) -> _C:
            if code in self.codes:
                raise DuplicateFileTypeCodeError(cls, code)

            logger.debug(f"Collecting the file type `{cls.__name__}` with the code `{code}`")
            self._types[code] = cls
            return cls

        return inner

    def __str__(self) -> str:
        return "\n".join(f"< {code} : {cls.__name__} >" for code, cls in self)

    def __iter__(self) -> Iterator[Tuple[str, DataFile]]:
        """
        Yields `str`, `DataFile` pairs where the `str` is the code
        corresponding to the `DataFile`
        """
        yield from self._types.items()

    def get_class(self, code: str) -> DataFile:
        """
        Given the provided `code`, returns the corresponding object
        Args:
            code: A `str` with the file code

        Returns:
            A `DataFile` object corresponding to the provided `code`

        Raises:
            InvalidFileTypeError if there is no corresponding class
            to the code
        """
        logger.debug(f"Getting class for code: {code}")
        if code in self._types:
            return self._types[code]
        raise InvalidFileTypeError(code)

    def get_code(self, file_class: DataFile) -> str:
        """
        Given the provided `DataFile`, returns the corresponding code
        Args:
            file_class: A `DataFile`
        Returns:
            A `str` object corresponding to the provided `DataFile`

        Raises:
            InvalidFileTypeError if there is no corresponding code
            to the class
        """
        logger.debug(f"Getting code for class {file_class}")
        for code, file in self._types.items():
            if file_class == file:
                return code
        raise InvalidFileTypeError(code)

    @property
    def codes(self) -> Tuple[str]:
        return tuple(self._types)

    @property
    def objects(self) -> Tuple[str]:
        return tuple(self._types.values())

from __future__ import annotations

import abc
import io
from pathlib import Path
from typing import Optional
from typing import Tuple

import pandas as pd
from tabulate import tabulate

from cat_file.filetypes._manager import filetype
from cat_file.logging import logger as _l
from cat_file.stream import zero_buffer

logger = _l.getChild(__name__)


class DataFile(abc.ABC):
    """
    A class implementation of a DataFile.
    """

    def __init__(self, contents: pd.DataFrame, path: Optional[Path] = None) -> None:
        self._contents = contents
        self._path = Path(path) if path is not None else path

    @property
    def contents(self) -> pd.DataFrame:
        return self._contents

    @property
    def path(self) -> Path:
        return self._path

    @property
    def columns(self) -> Tuple[str]:
        return tuple(self.contents.columns)

    @property
    def code(self) -> str:
        return filetype.get_code(self)

    def __eq__(self, other) -> bool:
        return self._contents.equals(other._contents)

    def __getitem__(self, item) -> pd.DataFrame:
        return self.contents.iloc[item]

    def print(self, num_lines: Optional[int] = None) -> None:
        if num_lines is None or num_lines >= 0:
            df = self.contents.head(num_lines)
        else:
            df = self.contents.tail(abs(num_lines))

        logger.debug(f"Printing {df.shape[0]} lines")
        print("~" * 50, end="\n\n")
        print(tabulate(df, headers="keys", tablefmt="grid", stralign="center", numalign="center", missingval="null"))

    def describe(self) -> None:
        """
        Describes:
         1. The number of rows
         2. The number of columns
         3. The names of the columns
         4. Null count per column
         5. Number of unique values per column
        """
        logger.debug("Describing data")
        output = pd.DataFrame(index=pd.Index(self.columns, name="Columns"))
        output["Null Count"] = self.contents.isnull().sum()
        output["# Unique"] = self.contents.nunique()
        print("~" * 100)
        print(f"\n\n\t# Rows: {self.contents.shape[0]:,}\n\t# Columns: {self.contents.shape[1]:,}\n\n")
        print(tabulate(output.sort_index(), headers="keys", tablefmt="grid", stralign="center", numalign="center"))

    @classmethod
    def from_bytes_stream(cls, buffer: io.BytesIO) -> DataFile:
        """
        An alternative constructor for the class for reading file streams

        Args:
            buffer: A `io.BytesIO` object
        """
        logger.debug(f"Loading the {cls.__name__} stream to a DataFrame")
        with zero_buffer(buffer) as b:
            try:
                return cls(cls.stream_to_dataframe(b))
            except Exception:
                logger.error("Loading failed :(")
                raise

    @staticmethod
    @abc.abstractmethod
    def is_valid_input(buffer: io.BytesIO) -> bool:
        """
        Determines if the provided `buffer` matches the the data file type
        Args:
            buffer: A `io.BytesIO` object with the contents of the file

        Returns:
            `True` if `buffer` meets the data file type; otherwise, `False`
        """

    @staticmethod
    @abc.abstractmethod
    def stream_to_dataframe(stream: io.BytesIO) -> pd.DataFrame:
        """
        Given a `io.BytesIO` object, loads it into a `pd.DataFrame` and returns the new object
        """

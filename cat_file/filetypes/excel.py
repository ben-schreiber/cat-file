from __future__ import annotations

import io
from zipfile import BadZipfile

import pandas as pd
from pandas.io.excel._base import inspect_excel_format

from cat_file.filetypes._base import DataFile
from cat_file.filetypes._manager import filetype
from cat_file.logging import logger as __logger
from cat_file.stream import zero_buffer

logger = __logger.getChild(__name__)


@filetype.register(code="xl")
class Excel(DataFile):
    @staticmethod
    def stream_to_dataframe(stream: io.BytesIO) -> pd.DataFrame:
        return pd.read_excel(stream)

    @staticmethod
    def is_valid_input(buffer: io.BytesIO) -> bool:
        with zero_buffer(buffer) as b:
            try:
                return inspect_excel_format(b.read()) is not None
            except (ValueError, BadZipfile):
                return False

from __future__ import annotations

import io

import pandas as pd

from cat_file.filetypes._base import DataFile
from cat_file.filetypes._manager import filetype
from cat_file.logging import logger as __logger
from cat_file.stream import zero_buffer

logger = __logger.getChild(__name__)


@filetype.register(code="p")
class Parquet(DataFile):
    @staticmethod
    def stream_to_dataframe(stream: io.BytesIO) -> pd.DataFrame:
        return pd.read_parquet(stream, engine="pyarrow")

    @staticmethod
    def is_valid_input(buffer: io.BytesIO) -> bool:
        with zero_buffer(buffer) as b:
            return b.read(3) == b"PAR"

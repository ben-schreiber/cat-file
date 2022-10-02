from __future__ import annotations

import io
import json

import pandas as pd

from cat_file.filetypes._base import DataFile
from cat_file.filetypes._manager import filetype
from cat_file.logging import logger as __logger
from cat_file.stream import zero_buffer

logger = __logger.getChild(__name__)


@filetype.register(code="jl")
class JSON_Lines(DataFile):
    @staticmethod
    def stream_to_dataframe(stream: io.BytesIO) -> pd.DataFrame:
        return pd.DataFrame.from_records(json.loads(row) for row in stream.readlines())

    @staticmethod
    def is_valid_input(buffer: io.BytesIO) -> bool:
        with zero_buffer(buffer) as b:
            if len(b.read()) == 0:
                return False

        with zero_buffer(buffer) as b:
            for line in b.read().decode().splitlines():
                if line.strip() != "" and (line[0] != "{" or line[-1] != "}"):
                    return False
        return True

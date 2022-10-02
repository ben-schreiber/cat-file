from __future__ import annotations

import csv
import io

import pandas as pd

from cat_file.filetypes._base import DataFile
from cat_file.filetypes._manager import filetype
from cat_file.logging import logger as __logger
from cat_file.stream import zero_buffer

logger = __logger.getChild(__name__)


@filetype.register(code="c")
class CSV(DataFile):
    @staticmethod
    def stream_to_dataframe(stream: io.BytesIO) -> pd.DataFrame:
        return pd.read_csv(stream)

    @staticmethod
    def is_valid_input(buffer: io.BytesIO) -> bool:
        try:
            sniffer = csv.Sniffer()
            with zero_buffer(buffer) as b:
                sample = b.read().decode()
                sniffer.sniff(sample)
                return sniffer.has_header(sample)
        except csv.Error:
            return False

import io
import json
from typing import Optional

import pandas as pd
import pytest

from cat_file.filetypes import DataFile
from cat_file.filetypes import filetype


def provide_buffer(func):
    def inner(data: pd.DataFrame, buffer: Optional[io.BytesIO] = None):
        if buffer is None:
            buffer = io.BytesIO()
        buffer = func(data, buffer)
        buffer.seek(0)
        return buffer

    return inner


class Convert:
    @staticmethod
    @provide_buffer
    def parquet(data: pd.DataFrame, buffer: Optional[io.BytesIO] = None) -> io.BytesIO:
        data.to_parquet(buffer)
        return buffer

    @staticmethod
    @provide_buffer
    def excel(data: pd.DataFrame, buffer: Optional[io.BytesIO] = None) -> io.BytesIO:
        with pd.ExcelWriter(buffer) as f:
            data.to_excel(f)
        return buffer

    @staticmethod
    @provide_buffer
    def csv(data: pd.DataFrame, buffer: Optional[io.BytesIO] = None) -> io.BytesIO:
        data.to_csv(buffer, index=False)
        return buffer

    @staticmethod
    @provide_buffer
    def json_lines(data: pd.DataFrame, buffer: Optional[io.BytesIO] = None) -> io.BytesIO():
        for line in data.to_dict(orient="records"):
            buffer.write(json.dumps(line).encode("utf-8"))
            buffer.write(b"\n")
        return buffer


@pytest.fixture
def data() -> pd.DataFrame:
    return pd.DataFrame({"a": list(range(5)), "b": list("abcde"), "c": [None] * 5})


@pytest.mark.parametrize("obj", filetype.objects)
def test_is_valid_input_correct_file_type(obj: DataFile, data: pd.DataFrame) -> None:
    stream = getattr(Convert, obj.__name__.lower())(data)
    assert obj.is_valid_input(stream)


@pytest.mark.parametrize("obj", filetype.objects)
def test_is_valid_input_wrong_file_type(obj: DataFile, data: pd.DataFrame) -> None:
    for other_file_type in filetype.objects:
        if other_file_type.__name__ != obj.__name__:
            wrong_data = getattr(Convert, other_file_type.__name__.lower())(data)
            try:
                is_valid = obj.is_valid_input(wrong_data)
            except Exception:
                is_valid = False
            assert not is_valid, f"{other_file_type.__name__ = }"

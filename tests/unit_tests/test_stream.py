import io
import os
import sys
from pathlib import Path
from tempfile import gettempdir
from typing import Optional

import pytest

from cat_file.stream import load_file_stream
from cat_file.stream import zero_buffer


@pytest.mark.parametrize("path", [None, os.path.join(gettempdir(), "cat-file_file.txt")])
def test_load_file_stream(monkeypatch, path: Optional[str]):
    data = b"fake data"

    class mock_stdin:
        def __init__(self, data: bytes):
            self.buffer = io.BytesIO(data)

    if path is None:
        monkeypatch.setattr("sys.stdin", mock_stdin(data))
        sys.stdin.buffer.write(data)
        sys.stdin.buffer.seek(0)
    else:
        Path(path).write_bytes(data)

    result = load_file_stream(path)
    assert result.read() == data


@pytest.mark.parametrize("read_position", list(range(15)))
def test_zero_buffer(read_position: int):
    data = b"more fake data"
    buffer = io.BytesIO(data)
    buffer.seek(read_position)

    with zero_buffer(buffer) as b:
        assert b.read() == data  # Assert buffer was zeroed out

    assert buffer.tell() == read_position

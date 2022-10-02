import os
from importlib import import_module
from typing import List

import pytest


def get_files_to_import() -> List[str]:
    output = []
    for dirpath, _, filenames in os.walk("cat_file"):
        if "__pycache__" not in dirpath:
            parent_name = dirpath.replace("/", ".")
            output.append(parent_name)
            output.extend(f"{parent_name}.{file.rstrip('.py')}" for file in filenames if file.endswith(".py"))
    return output


@pytest.mark.parametrize("module", get_files_to_import())
def test_imports(module: str) -> None:
    try:
        import_module(module)
    except Exception as e:
        assert False, e

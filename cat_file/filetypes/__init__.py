from importlib import import_module
from pathlib import Path

from cat_file.filetypes._base import DataFile
from cat_file.filetypes._manager import filetype


# IMPORTANT: We must import all file types in order that the `filetype` class can register them
for file in Path(__file__).parent.iterdir():
    if not file.name.startswith("_"):
        import_module(f"cat_file.filetypes.{file.stem}")

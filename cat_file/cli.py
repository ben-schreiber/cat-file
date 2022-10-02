import argparse

from cat_file.filetypes import filetype
from cat_file.logging import logger as __logger
from cat_file.utils import should_read_from_stdin


logger = __logger.getChild(__name__)


def create_parser() -> argparse.ArgumentParser:
    """
    Creates and returns a CLI parser object for the program

    Returns:
        An `argparse.ArgumentParser` object
    """
    parser = argparse.ArgumentParser(
        prog="cat-file",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
-------------------------------------------------------------------------------

A CLI tool to help read and cat files without having to download them.
This program can be used in one of two ways:

(1) By piping raw data into it
(2) By directly running the program and providing it with a path

Additionally, a file type flag can be passed to the program. In such a case,
the program will directly attempt to read the file according to the given code.
Otherwise, the program will attempt to infer the file's type.
* See the `optional arguments` for the available file type flags

-------------------------------------------------------------------------------
    """,
    )

    codes_group = parser.add_mutually_exclusive_group()
    for code, file_type in filetype:
        codes_group.add_argument(
            f"-{code}",
            f"--{file_type.__name__.lower()}",
            action="store_const",
            const=code,
            help=f"flag for `{file_type.__name__.replace('_', ' ').lower()}` file",
            dest="file_type_flag",
        )

    head_tail_group = parser.add_mutually_exclusive_group()
    head_tail_group.add_argument(
        "--head",
        help=f"Number of lines to print starting from the beginning of the file. Default is 5",
        nargs="?",
        type=int,
        const=5,
        metavar="N",
    )
    head_tail_group.add_argument(
        "--tail",
        help=f"Number of lines to print starting from the end of the file. Default is 5",
        nargs="?",
        type=int,
        const=-5,
        metavar="N",
    )

    head_tail_group.add_argument("--describe", help="Describe the metadata of the file", action="store_true")
    if not should_read_from_stdin():
        parser.add_argument(
            "path",
            nargs=1,
            type=str,
            help="The path of the file to inspect. Can be either local or in S3",
        )
    return parser


def get_args() -> argparse.Namespace:
    """
    Returns:
        An `argparse.Namespace` object with the args from the CLI
    """
    return create_parser().parse_args()

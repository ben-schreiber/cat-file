#! /usr/bin/env python3
from cat_file.cat_file import CatFile
from cat_file.cli import get_args
from cat_file.stream import load_file_stream
from cat_file.utils import get_num_lines_to_print
from cat_file.utils import get_path_from_args


def main() -> None:
    args = get_args()
    cf = CatFile(
        buffer=load_file_stream(get_path_from_args(args)),
        file_type_flag=args.file_type_flag,
        describe=args.describe,
        num_lines_to_print=get_num_lines_to_print(args),
    )
    cf.run()


if __name__ == "__main__":
    main()

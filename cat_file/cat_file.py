import io
from typing import Optional
from typing import Union

from cat_file.errors import NoFileTypeFoundError
from cat_file.filetypes import filetype
from cat_file.logging import logger as __logger


logger = __logger.getChild(__name__)


class CatFile:
    def __init__(
        self,
        buffer: io.BytesIO,
        file_type_flag: Optional[str] = None,
        describe: bool = False,
        num_lines_to_print: Optional[int] = None,
    ) -> None:
        self._buffer = buffer
        self._file_type_flag = file_type_flag
        self._file = None
        self._describe = describe
        self._num_lines_to_print = num_lines_to_print

    def set_file_type(self) -> None:
        """
        Sets the file type variable in the class
        """
        logger.info("Determining the file type of the provided input")
        suspected_file_type = self._sniff_file_type()
        if self._file_type_flag is not None:
            if self._file_type_flag == suspected_file_type:
                logger.debug(f"File type already determined, continuing...")
            else:
                logger.warning(
                    f"The provided file type flag ('{self._file_type_flag}') does not seem to match the actual file type ('{suspected_file_type}')"
                )
        elif suspected_file_type is not None:
            self._file_type_flag = suspected_file_type
        else:
            raise NoFileTypeFoundError()

    def _sniff_file_type(self) -> Union[str, None]:
        """
        Returns:
            A `str` with the suspected file type.
        """
        for code, cls in filetype:
            logger.debug(f"Checking if {cls.__name__} is the correct file type")
            if cls.is_valid_input(self._buffer):
                logger.debug(f"The file type {cls.__name__} matches the given input")
                return code

    def load_file_from_buffer(self) -> None:
        logger.info("Loading the file from the buffer into a DataFrame")
        if self._file_type_flag is None:
            raise NoFileTypeFoundError()

        cls = filetype.get_class(self._file_type_flag)
        self._file = cls.from_bytes_stream(self._buffer)

    def print_file_to_screen(self) -> None:
        if self._describe:
            self._file.describe()
        else:
            self._file.print(num_lines=self._num_lines_to_print)

    def run(self) -> None:
        self.set_file_type()
        self.load_file_from_buffer()
        self.print_file_to_screen()

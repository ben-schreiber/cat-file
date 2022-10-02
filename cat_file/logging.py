import logging
import os
import sys


class ColoredFormatter(logging.Formatter):

    BLUE = "\x1b[34;1m"
    YELLOW = "\x1b[33;1m"
    GREEN = "\x1b[32;1m"
    RED = "\x1b[31;1m"
    _FORMAT = "[{color}%(levelname)s\x1b[0m][%(asctime)s][%(name)s] %(message)s"

    FORMATS = {
        logging.DEBUG: _FORMAT.format(color=BLUE),
        logging.INFO: _FORMAT.format(color=GREEN),
        logging.WARNING: _FORMAT.format(color=YELLOW),
        logging.ERROR: _FORMAT.format(color=RED),
    }

    def format(self, record) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", logging.WARNING))
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(ColoredFormatter())
logger.addHandler(console_handler)

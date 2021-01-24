import logging
import logging.config
import logging.handlers

from profile_generator.util import file

_LOG_DIR = "logs"


class SingleLevelFilter(logging.Filter):
    def __init__(self, level: str):
        super().__init__()
        self.level = level

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelname == self.level


_CONFIG = {
    "version": 1,
    "formatters": {
        "stderr": {"class": "logging.Formatter", "format": "ERROR %(message)s"},
        "detailed": {
            "class": "logging.Formatter",
            "format": "%(asctime)s | %(name)-15s | %(levelname)-8s | %(message)s",
        },
    },
    "filters": {
        "infoOnly": {
            "()": SingleLevelFilter,
            "level": "INFO",
        },
        "errorOnly": {
            "()": SingleLevelFilter,
            "level": "ERROR",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "INFO",
            "filters": ["infoOnly"],
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": "ERROR",
            "filters": ["errorOnly"],
            "formatter": "stderr",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": file.join(_LOG_DIR, "profile_generator.log"),
            "mode": "w",
            "formatter": "detailed",
        },
    },
    "loggers": {
        "console": {
            "handlers": ["stdout", "stderr"],
        },
    },
    "root": {"level": "INFO", "handlers": ["file"]},
}


def init() -> None:
    file.create_dir(_LOG_DIR)
    logging.config.dictConfig(_CONFIG)


def get_console_logger() -> logging.Logger:
    return logging.getLogger("console")

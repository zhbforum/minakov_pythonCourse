import logging
import os

from constants import LOGGER_NAME, LOG_FILE_PATH, LOG_FORMAT, DEFAULT_ENCODING


def init_logger() -> logging.Logger:
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(LOG_FILE_PATH, encoding=DEFAULT_ENCODING)
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = init_logger()

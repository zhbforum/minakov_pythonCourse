import logging
from constants import LOGGER_NAME, LOG_FILE_PATH, LOG_FORMAT, DEFAULT_ENCODING


def init_logger() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(LOG_FILE_PATH, encoding=DEFAULT_ENCODING)
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = init_logger()

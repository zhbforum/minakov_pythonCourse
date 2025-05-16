import logging
from constants import LOG_FORMAT, DEFAULT_LOG_FILE


def setup_logger(log_level="INFO", log_file=DEFAULT_LOG_FILE):
    """
    Set up and return a logger that logs to both console and file.

    Args:
        log_level (str): Logging level (e.g., 'DEBUG', 'INFO').
        log_file (str): Path to the log file.

    Returns:
        logging.Logger: Configured logger.
    """
    log = logging.getLogger('lab_3_logger')
    log.setLevel(log_level.upper())
    
    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    return log

import logging
import sys


def get_logger(name="root", level=logging.DEBUG):
    """Creates and returns a logger with stream handler.

    Args:
    name (str): Name of the logger. Default is 'root'.
    level (int): Logging level. Default is logging.INFO.

    Returns:
    logging.Logger: Configured logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

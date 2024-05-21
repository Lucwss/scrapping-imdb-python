import logging
import sys


def set_formatter(format: str, date_format: str):
    return logging.Formatter(format, date_format)


def setup_logging(level=logging.INFO):
    """
    :param level: Logging level  to be set for the application
    """

    formatter = set_formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[stream_handler])

    return logging.getLogger()


logger = setup_logging()

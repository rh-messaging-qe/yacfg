import logging
from logging.handlers import RotatingFileHandler
from typing import Optional


def config_console_logger(
    filename: Optional[str] = None,
    fmt: Optional[str] = None,
    fmt_color: Optional[str] = None,
    datefmt: Optional[str] = None,
    level=logging.DEBUG,
    max_bytes: int = 50000,
    backup_count: int = 3,
) -> None:
    """
    Configure a console and file logger with optional color support and rotating file handler.
    If colorlog is installed, it will use colorlog for colored output.

    :param filename: Stream to log into, default is sys.stdout.
    :param level: Console log level.
    :param fmt: Console log format.
    :param fmt_color: Console color log format (only with colorlog).
    :param datefmt: Formatter date format, default is ISO8601.
    :param max_bytes: Maximum log file size before rotation, default is 50000.
    :param backup_count: Number of backup log files to keep, default is 3.
    """

    level = level or logging.DEBUG
    fmt = fmt or "[%(asctime)s] [%(levelname)s] %(name)s :: %(message)s"
    fmt_color = fmt_color or (
        "[%(asctime)s] [%(log_color)s%(levelname)s%(reset)s] %(name)s :: %(message)s"
    )
    datefmt = datefmt or "%H:%M:%S"

    try:
        import colorlog  # type: ignore
        import colorama  # type: ignore

        colorama.init()

        # Create the console_formatter with the extended log_colors
        console_formatter = colorlog.ColoredFormatter(
            fmt_color,
            log_colors={
                "CRITICAL": "black,bg_red",
                "ERROR": "red",
                "WARNING": "yellow",
                "SKIP": "blue",
                "FAIL": "bold_red",
                "PASS": "bold_green",
                "INFO": "reset",
                "DOC": "purple",
                "DEBUG": "cyan",
            },
            reset=True,
            datefmt=datefmt,
        )

    except ImportError:
        import sys

        console_formatter = logging.Formatter(fmt, datefmt=datefmt)

    console_handler: logging.Handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    # Set default logger
    logging.getLogger().setLevel(level)

    # Add the console_handler to the logger
    logging.getLogger().addHandler(console_handler)

    # File logging
    if filename:
        file_handler = RotatingFileHandler(
            filename, maxBytes=max_bytes, backupCount=backup_count
        )
        file_formatter = logging.Formatter(fmt, datefmt=datefmt)
        file_handler.setFormatter(file_formatter)
        logging.getLogger().addHandler(file_handler)

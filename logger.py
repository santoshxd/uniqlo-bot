import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger("uniqlo_bot")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console log
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # File log (rotates at 2MB, keeps 5 files)
    file_handler = RotatingFileHandler(
        "bot.log",
        maxBytes=2 * 1024 * 1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

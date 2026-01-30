import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")  # you can change to backend/logs or absolute path
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

# Cache loggers so you don’t attach handlers 200 times
_LOGGER_CACHE = {}


def get_logger(name: str = "app") -> logging.Logger:
    """
    Returns a configured logger with file + console handlers.
    Rotates logs daily and keeps only last 3 days.
    """
    if name in _LOGGER_CACHE:
        return _LOGGER_CACHE[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs if root logger is configured too
    logger.propagate = False

    # Very important: avoid adding multiple handlers again & again
    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # ✅ Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # ✅ File handler with daily rotation
        file_handler = TimedRotatingFileHandler(
            filename=str(LOG_FILE),
            when="midnight",       # rotate at midnight
            interval=1,            # every day
            backupCount=3,         # ✅ keep only last 3 backups
            encoding="utf-8",
            utc=False
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    _LOGGER_CACHE[name] = logger
    return logger

"""Default logger config.."""

import logging
from logging.config import dictConfig

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
        },
        "detailed": {
            "format": "[%(asctime)s] %(levelname)s - %(name)s - %(filename)s - %(lineno)d - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "level": "INFO",
            "filename": "app.log",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
    "loggers": {
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

dictConfig(logging_config)
logger = logging.getLogger("backend")

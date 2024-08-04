import logging
import logging.config
from datetime import datetime

from scripts.config import Config


def setup_logging():
    """Setup logging configuration"""
    log_filename = f"app_log_{datetime.now().strftime('%Y-%m-%d')}.log"

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "file_handler": {
                "class": "logging.FileHandler",
                "formatter": "standard",
                "level": "INFO",
                "filename": log_filename,
                "mode": "a"
            }
        },
        "loggers": {
            "": {
                "handlers": ["file_handler"],
                "level": "INFO",
                "propagate": True
            }
        }
    }

    logging.config.dictConfig(logging_config)
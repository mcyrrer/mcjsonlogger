# Filename: logger_setup.py
# Author:   Mattias Gustavsson
# Created:  2024-01-01
# Modified: 2024-01-01
# License:  MIT
# Description:
#   Set up a logger with a customized JSON formatter. 

import logging
import json

class JSONFormatter(logging.Formatter):
    """
    Customized JSON formatter for logging.
    """
    def __init__(self, *args, column_names=None, **kwargs):
        self.column_names = column_names or []
        super().__init__(*args, **kwargs)

    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "filename": record.filename,
            "lineno": record.lineno,
        }

        # Inject additional columns with non-empty values
        for col_name in self.column_names:
            value = getattr(record, col_name, "")
            if value:
                log_record[col_name] = value

        return json.dumps(log_record)

class LoggerSetup:
    def __init__(self, level=logging.DEBUG, column_names=None):
        self.level = level
        self.column_names = column_names or []
        self.logger = None

    def configure_logger(self):
        logging.basicConfig(level=self.level)

        # Remove existing handlers to avoid duplicate logs
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Add a new handler with the customized JSON formatter
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter(column_names=self.column_names))
        logging.root.addHandler(handler)

        # Set the logger instance
        self.logger = logging.getLogger()

    def get_logger(self):
        if not self.logger:
            self.configure_logger()
        return self.logger if self.logger else logging.getLogger()

# Singleton pattern to ensure only one instance of the logger setup is used
logger_setup_instance = LoggerSetup()

def setup_and_get_logger(column_names=None, level=logging.DEBUG):
    """
    Set up and get a logger instance.

    Args:
        column_names (list): Additional column names for the JSON log format.
        level (int): Logging level (e.g., logging.DEBUG, logging.INFO).

    Returns:
        logging.Logger: Logger instance.
    """
    if column_names is None:
        column_names = ['stacktrace']
    else:
        column_names.append('stacktrace')
    logger_setup_instance.column_names = column_names or []
    logger_setup_instance.level = level
    return logger_setup_instance.get_logger()

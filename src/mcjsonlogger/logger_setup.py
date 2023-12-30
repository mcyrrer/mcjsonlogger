# mylogger/setup/logger_setup.py
import logging
import json

class JSONFormatter(logging.Formatter):
    def __init__(self, *args, column_names=None, **kwargs):
        self.column_names = column_names or []
        super().__init__(*args, **kwargs)

    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "serverity": record.levelname,
            "message": record.getMessage(),
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
        return self.logger

# Singleton pattern to ensure only one instance of the logger setup is used
logger_setup_instance = LoggerSetup()

def setup_and_get_logger(column_names=None):
    logger_setup_instance.column_names = column_names or []
    return logger_setup_instance.get_logger()

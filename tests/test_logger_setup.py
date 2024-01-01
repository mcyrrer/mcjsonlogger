# tests/test_logger_setup.py
import json
import logging
import unittest
from io import StringIO
from unittest.mock import patch

from src.mcjsonlogger.logger_setup import JSONFormatter, LoggerSetup, setup_and_get_logger


class TestLoggerSetup(unittest.TestCase):
    def setUp(self):
        # Reset the logging configuration before each test
        logging.root.handlers = []

    def test_configure_logger(self):
        setup_instance = LoggerSetup()
        setup_instance.configure_logger()

        # Assert that a handler has been added to the root logger
        self.assertTrue(logging.root.handlers)

        # Check that the handler uses the correct formatter
        handler = logging.root.handlers[0]
        self.assertIsInstance(handler.formatter, JSONFormatter)

    def test_get_logger(self):
        setup_instance = LoggerSetup()
        logger = setup_instance.get_logger()

        # Assert that the returned logger is an instance of logging.Logger
        self.assertIsInstance(logger, logging.Logger)

    def test_setup_and_get_logger(self):
        # Patch the configure_logger method to avoid actual configuration
        with patch.object(LoggerSetup, 'configure_logger'):
            logger = setup_and_get_logger()

        # Assert that the returned logger is an instance of logging.Logger
        self.assertIsInstance(logger, logging.Logger)

    def test_logging_output_with_extra_columns(self):
        setup_instance = LoggerSetup(column_names=['user_id', 'request_id'])
        setup_instance.configure_logger()
        logger = setup_instance.get_logger()

        # Use a StringIO to capture the log output
        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setFormatter(JSONFormatter(column_names=setup_instance.column_names))
        logger.addHandler(handler)

        try:
            logger.info("Test message", extra={'user_id': '123', 'request_id': '456'})

            # Retrieve the logs from the StringIO
            log_output = json.loads(log_stream.getvalue().strip())
            # Check that the expected columns are present in the log output
            self.assertIn('user_id', log_output)
            self.assertEqual(log_output['user_id'], '123')
            self.assertIn('request_id', log_output)
            self.assertEqual(log_output['request_id'], '456')
            self.assertIn('Test message', log_output['message'])
        finally:
            logger.removeHandler(handler)

    def test_logging_output(self):
        setup_instance = LoggerSetup()
        setup_instance.configure_logger()
        logger = setup_instance.get_logger()

        # Use a StringIO to capture the log output
        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setFormatter(JSONFormatter(column_names=setup_instance.column_names))
        logger.addHandler(handler)

        try:
            logger.info("Test message", extra={'user_id': '123', 'request_id': '456'})

            # Retrieve the logs from the StringIO
            log_output = json.loads(log_stream.getvalue().strip())
            # Check that the expected columns are present in the log output
            self.assertNotIn('user_id', log_output)
            self.assertNotIn('request_id', log_output)
            self.assertIn('Test message', log_output['message'])

        finally:
            logger.removeHandler(handler)

    def test_log_level(self):
        # Set up logger with a specific logging level
        logger = setup_and_get_logger(level=logging.WARNING)

        # Use a StringIO to capture the log output
        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setFormatter(JSONFormatter(column_names=['level']))
        logger.addHandler(handler)

        try:
            # Log messages with different levels
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")

            # Retrieve the logs from the StringIO
            log_output = json.loads(log_stream.getvalue().strip().split('\n')[-1])

            # Check that the log level is WARNING
            self.assertEqual(log_output['level'], 'WARNING')

            # Additional assertion: Ensure DEBUG log is not present in the output
            self.assertNotIn('DEBUG', log_stream.getvalue())
        finally:
            logger.removeHandler(handler)

if __name__ == '__main__':
    unittest.main()

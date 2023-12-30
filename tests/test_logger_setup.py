# tests/test_logger_setup.py
import unittest
import logging
import json
from io import StringIO

from unittest.mock import patch

from src.mcjsonlogger.logger_setup import LoggerSetup, JSONFormatter


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
            logger = LoggerSetup().get_logger()

        # Assert that the returned logger is an instance of logging.Logger
        self.assertIsInstance(logger, logging.Logger)

    def test_logging_output(self):
        setup_instance = LoggerSetup(column_names=['user_id', 'request_id'])
        setup_instance.configure_logger()
        logger = setup_instance.get_logger()

        # Use a StringIO to capture the log output
        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setFormatter(JSONFormatter())
        logging.root.addHandler(handler)

        try:
            logger.info("Test message", extra={'user_id': '123', 'request_id': '456'})

            # Retrieve the logs from the StringIO
            log_output = json.loads(log_stream.getvalue().strip())
            print(f"Log output: {log_output}")
            # Check that the expected columns are present in the log output
            self.assertIn('user_id', log_output)
            self.assertEqual(log_output['user_id'], '123')
            self.assertIn('request_id', log_output)
            self.assertEqual(log_output['request_id'], '456')
        finally:
            logging.root.removeHandler(handler)

if __name__ == '__main__':
    unittest.main()

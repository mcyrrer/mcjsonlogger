# mcjsonlogger - JSON logger for Python

Simple JSON logger for Python. This is a wrapper around the standard Python
logging module that outputs JSON-formatted log messages to stdout and it main purpose is to 
have a simple wrapper class to be used in Kubernetes in many python apps where it is
easy to add new columns.

## Example usage
    
```python
    # Example of how to use the mcjsonlogger in another file
    from mcjsonlogger import setup_and_get_logger

    # Set up logging and get the logger
    # level defaults to logging.DEBUG
    # column_names defaults to none.
    logger = setup_and_get_logger(level=logging.DEBUG, column_names=['user_id', 'request_id'])

    def example_function(user_id, request_id):
        logger.info("This is an info message", extra={'user_id': user_id, 'request_id': request_id})
        logger.warning("This is a warning message")
        try:
            raise Exception("This is an exception")
        except Exception as e:
            logger.error("This is an error message", extra={'stacktrace': traceback.format_exc()})        

    if __name__ == "__main__":
        example_function(user_id="123", request_id="456")
```
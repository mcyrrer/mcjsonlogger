# mcjsonlogger - JSON logger for Python

Simple JSON logger for Python.  This is a wrapper around the standard Python
logging module that outputs JSON-formatted log messages.

Main purpose is to have a simple wrapper class where it is easy to add new columns.

## Example usage
    
```python
    # Example of how to use the mcjsonlogger in another file
    from mcjsonlogger import setup_and_get_logger

    # Set up logging and get the logger
    logger = setup_and_get_logger(column_names=['user_id', 'request_id'])

    def example_function(user_id, request_id):
        logger.info("This is an info message", extra={'user_id': user_id, 'request_id': request_id})
        logger.warning("This is a warning message")

    if __name__ == "__main__":
        example_function(user_id="123", request_id="456")
```
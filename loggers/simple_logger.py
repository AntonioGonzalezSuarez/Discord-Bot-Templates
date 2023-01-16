import logging


def start_logger():
    # Create a custom logger
    logger = logging.getLogger()

    # Create handlers
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter("%(asctime)s -  %(message)s")
    c_handler.setFormatter(c_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    return logger

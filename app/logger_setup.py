import os
import logging


def set_logger_level(logger_to_set):
    """Get logging_level from environment and use to set the logging level."""
    logging_level = os.getenv('logging_level', 'NONE').upper()
    if logging_level == 'NONE':
        print("No logging_level environmental variable found. Defaulting to 'DEBUG'.")
        logging_level = 'DEBUG'
    else:
        print("Setting logger to level: %s." % logging_level)
    logging_level_name = logging.getLevelName(logging_level)
    logger_to_set.setLevel(logging_level_name)
    return


def set_logger_format(logger_to_format):
    """Set logger output format to a hardcoded version."""
    print("Setting logger formatting")
    log_format = logging.Formatter(fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                                   datefmt='%d-%b-%y %H:%M:%S')
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(log_format)
    logger_to_format.addHandler(log_handler)
    return

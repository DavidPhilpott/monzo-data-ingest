import boto3
import os
import logging
import requests
import json


def set_logger_level(logger_to_set):
    """Get logging_level from environment and use to set the logging level."""
    logging_level = os.getenv('logging_level', 'NONE').upper()
    if logging_level is 'NONE':
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


def get_ssm_parameter_value(parameter_name):
    """Make a get request to SSM for the given parameter and return un-encrypted value"""
    logger.info("Seeking SSM value for environmental variable '%s'." % parameter_name)
    try:
        parameter_env = os.getenv(parameter_name, None)
        if parameter_env is not None:
            logger.debug("Found environmental variable. Associated value is set to '%s'" % parameter_env)
        else:
            raise ValueError("Could not find value for environmental variable '%s'" % parameter_name)
    except ValueError as e:
        logger.exception(e, exc_info=False)
        raise e
    logger.debug("Creating SSM client.")
    ssm_client = boto3.client('ssm')
    logger.debug("Requesting un-encrypted parameter information for '%s'." % parameter_env)
    parameter_info = ssm_client.get_parameter(Name=parameter_env, WithDecryption=True)
    logger.debug("Returned parameter_info dictionary. Seeking ['Parameter']['Value'].")
    parameter_value = parameter_info['Parameter']['Value']
    logger.info("Value found. Returning...")
    return parameter_value

def main(event, context):
    print("-- Instantiating logger --")
    global logger
    logger = logging.getLogger(__name__)
    logger.propagate = False
    set_logger_level(logger)
    set_logger_format(logger)

    logger.info("-- Getting Parameter Values --")
    sns_topic_arn = get_ssm_parameter_value(parameter_name='target_sns_arn_parameter')
    logger.info("Finished getting parameter values.")

    logger.info("-- Placeholder --")
    logger.info("Function finished.")
    return
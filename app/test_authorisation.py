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


def authorisation_test(access_key):
    """Submit a request to monzo whoami. Return true if monzo allows access, false otherwise"""
    """TODO: Change this exception handling to check for http error codes coming back from requests"""
    logger.info("Testing access to Monzo.")
    api_url = r'https://api.monzo.com/ping/whoami'
    test_params = {'Authorization': 'Bearer %s' % access_key}
    try:
        logger.debug("Making request to whoami API.")
        logger.debug("URL: %s, Parameters: %s" % (api_url, test_params.keys()))
        access_test = requests.get(url=api_url, headers=test_params)
        result = json.loads(access_test.text)['authenticated']
        logger.debug("Received authorisation result '%s'" % result)
    except Exception as e:
        logger.warning(e, exc_info=False)
        logger.debug("Setting result to 'False' by default.")
        result = False
        pass
    logger.debug("Returning %s." % result)
    return result


def main(event, context):
    print("-- Instantiating logger --")
    global logger
    logger = logging.getLogger(__name__)
    logger.propagate = False
    set_logger_level(logger)
    set_logger_format(logger)

    logger.info("-- Getting Parameter Values --")
    access_key = get_ssm_parameter_value(parameter_name='access_key_parameter')
    logger.info("Finished getting parameter values.")

    logger.info("-- Testing Current Access Keys --")
    if authorisation_test(access_key) is True:
        logger.info("Authorisation test PASSED. Keys do not need to be refreshed.")
        return {"auth_granted": "true"}
    else:
        logger.info("Authorisation test FAILED. Keys need to be refreshed.")
        return {"auth_granted": "false"}

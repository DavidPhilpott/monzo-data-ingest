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
    log_format = logging.Formatter(fmt='%(asctime)s | %(levelname)s | %(message)s',
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


def refresh_access_key(client_id, client_secret_id, refresh_token):
    """Submit refresh token to Monzo in exchange for a new access key and refresh token"""
    logger.info("Exchanging refresh token with Monzo.")
    api_url = 'https://api.monzo.com/oauth2/token'
    refresh_params = {'grant_type': 'refresh_token',
                      'client_id': client_id,
                      'client_secret': client_secret_id,
                      'refresh_token': refresh_token}
    logging.debug("Submitting to '%s'" % api_url)
    raw_result = requests.post(url=api_url, data=refresh_params)
    logging.debug("Received result. Parsing JSON.")
    result = json.loads(raw_result.text)
    logging.debug("Returning access_token and refresh_token.")
    return result['access_token'], result['refresh_token']


def write_ssm_parameter_value(parameter_name, new_parameter_value, is_secure):
    """Write a parameter value to a given parameter name"""
    logger.info("Writing SSM parameter value for %s." % parameter_name)
    logger.debug("Searching for environmental variable.")
    try:
        parameter_env = os.getenv(parameter_name, None)
        if parameter_env is not None:
            logger.debug("Found environmental variable. Associated value is set to '%s'" % parameter_env)
        else:
            raise ValueError("Could not find value for environmental variable '%s'" % parameter_name)
    except ValueError as e:
        logger.exception(e, exc_info=False)
        raise e
    logging.debug("Requesting SSM client.")
    ssm_client = boto3.client('ssm')
    logger.debug("Argument is_secure is %s." % is_secure)
    if is_secure is False:
        string_type = "SecureString"
    else:
        string_type = "String"
    logging.debug("Writing value to SSM for %s. Type is %s" % (parameter_env, string_type))
    response = ssm_client.put_parameter(Name=parameter_env,
                                        Value=new_parameter_value,
                                        Type=string_type,
                                        Overwrite=True)
    logger.debug("Write response: %s" % response)
    logger.info("Write finished.")
    return


def main(event, context):
    print("-- Instantiating logger --")
    global logger
    logger = logging.getLogger(__name__)
    logger.propagate = False
    set_logger_level(logger)
    set_logger_format(logger)

    logger.info("-- Getting Parameter Values --")
    client_id = get_ssm_parameter_value(parameter_name='client_id_parameter')
    client_secret_id = get_ssm_parameter_value(parameter_name='client_secret_id_parameter')
    refresh_token = get_ssm_parameter_value(parameter_name='refresh_token_parameter')
    logger.info("Finished getting parameter values.")
    logger.info("-- Getting New Access Tokens --")
    new_access_key, new_refresh_token = refresh_access_key(client_id=client_id,
                                                           client_secret_id=client_secret_id,
                                                           refresh_token=refresh_token)
    logger.info("Finished getting new access tokens.")
    logger.info("-- Writing New Tokens to SSM -- ")
    write_ssm_parameter_value(parameter_name='access_key_parameter',
                              new_parameter_value=new_access_key,
                              is_secure=True)
    write_ssm_parameter_value(parameter_name='refresh_token_parameter',
                              new_parameter_value=new_refresh_token,
                              is_secure=True)
    return

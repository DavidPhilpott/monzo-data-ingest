import boto3
import os
import logging


def set_logger_level(log):
    """Get logging_level from environment and use to set the logging level."""
    logging_level = os.getenv('logging_level', 'NONE').upper()
    if logging_level is 'NONE':
        print("No logging_level environmental variable found. Defaulting to 'DEBUG'.")
        logging_level = 'DEBUG'
    logging_level_name = logging.getLevelName(logging_level)
    print("Setting logger to level: %s." % logging_level_name)
    log.setLevel(logging_level_name)
    return


def get_ssm_parameter_value(parameter_name):
    """Make a get request to SSM for the given parameter and return un-encrypted value"""
    logger.info("Seeking SSM value for environmental variable '%s'." % parameter_name)
    try:
        parameter_env = os.getenv(parameter_name, None)
        if parameter_env is not None:
            logger.debug("Found environmental variable. Associated value is set to '%s'" %s)
        else:
            raise ValueError("Could not find value for environmental variable '%s'" %parameter_name)
    except ValueError as e:
        logger.exception(e.message, exc_info=False)
        raise e
    logger.debug("Creating SSM client.")
    ssm_client = boto3.client('ssm')
    logger.debug("Requesting un-encrypted parameter information for '%s'." %parameter_env)
    parameter_info = ssm_client.get_parameter(Name=parameter_env, WithDecryption=True)
    logger.debug("Returned parameter_info.")
    logger.debug("Seeking parameter_info[parameter][value].")
    parameter_value = parameter_info['parameter']['value']
    logger.debug("Value found. Returning...")
    return parameter_value


def main(event, context):
    print("Instantiating logger.")
    global logger
    logger = logging.getLogger(__name__)
    set_logger_level(logger)

    logger.info("## Getting Parameter Values ##")
    client_id = get_ssm_parameter_value(parameter_name='client_id_parameter')
    client_secret_id = get_ssm_parameter_value(parameter_name='client_secret_id_parameter')
    redirect_uri = get_ssm_parameter_value(parameter_name='redirect_uri_parameter')
    access_key = get_ssm_parameter_value(parameter_name='access_key_parameter')
    refresh_token = get_ssm_parameter_value(parameter_name='refresh_token_parameter')

    print(client_id, client_secret_id, redirect_uri, access_key, refresh_token)
    return

import boto3
import os
import logging


def set_logger_level(log):
    """Get logging_level from environment and use to set the logging level."""
    logging_level = os.getenv('logging_level', 'NONE').Upper()
    if logging_level is 'NONE':
        print("No logging_level environmental variable found. Defaulting to 'DEBUG'.")
        logging_level = 'DEBUG'
    logging_level_name = logging.getLevelName(logging_level)
    print("Setting logger to level: %s." % logging_level_name)
    log.setLevel(logging_level_name)
    return


def get_ssm_parameter_value(parameter_name):
    """Make a get request to SSM for the given parameter and return un-encrypted value"""
    logger.info("Seeking value for %s." % parameter_name)
    logger.debug("Creating SSM client.")
    ssm_client = boto3.client('ssm')
    logger.debug("Requesting un-encrypted parameter information from SSM.")
    parameter_info = ssm_client.get_parameter(Name=parameter_name,
                                              WithDecryption=True)
    logger.debug("Returned parameter_info = %s." % str(parameter_info))
    logger.debug("Seeking parameter_info[parameter][value].")
    parameter_value = parameter_info['parameter']['value']
    logger.debug("Final parameter_value is %s." % parameter_value)
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

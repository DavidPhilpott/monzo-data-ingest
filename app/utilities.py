import logging
import logger_setup as logger_setup
import boto3
import os
logger = logging.getLogger(__name__)
logger.propagate = False
logger_setup.set_logger_level(logger)
logger_setup.set_logger_format(logger)


def get_environmental_variable_value(variable_name):
    """Attempt to get value of variable from os.env and return"""
    logger.info("Searching for environmental variable '%s'." % variable_name)
    try:
        variable_env_value = os.getenv(variable_name, None)
        if variable_env_value is not None:
            logger.info("Found variable value. Returning.")
            logger.debug("Associated value is set to '%s'." % variable_env_value)
        else:
            raise ValueError("Could not find value for environmental variable '%s'." % variable_name)
    except ValueError as e:
        logger.exception(e, exc_info=False)
        raise e
    return variable_env_value


def write_ssm_parameter_value(parameter_name, new_parameter_value, is_secure):
    """Write a parameter value to a given parameter name"""
    logger.info("Writing SSM parameter value for %s." % parameter_name)
    logging.debug("Requesting SSM client.")
    ssm_client = boto3.client('ssm')
    logger.debug("Argument is_secure is %s." % is_secure)
    if is_secure is True:
        string_type = "SecureString"
    else:
        string_type = "String"
    logging.debug("Writing value to SSM for %s. Type is %s" % (parameter_name, string_type))
    response = ssm_client.put_parameter(Name=parameter_name,
                                        Value=new_parameter_value,
                                        Type=string_type,
                                        Overwrite=True)
    logger.debug("Write response: %s" % response)
    logger.info("Write finished.")
    return


def write_ssm_parameter_value_from_env(parameter_name, new_parameter_value, is_secure):
    """Write a parameter value to a given parameter name"""
    parameter_env = get_environmental_variable_value(variable_name=parameter_name)
    write_ssm_parameter_value(parameter_name=parameter_env,
                              new_parameter_value=new_parameter_value,
                              is_secure=is_secure)
    return


def get_ssm_parameter_value(parameter_name):
    """Make a get request to SSM for the given parameter and return un-encrypted value"""
    logger.info("Seeking SSM value for environmental variable '%s'." % parameter_name)
    logger.debug("Creating SSM client.")
    ssm_client = boto3.client('ssm')
    logger.debug("Requesting un-encrypted parameter information for '%s'." % parameter_name)
    parameter_info = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
    logger.debug("Returned parameter_info dictionary. Seeking ['Parameter']['Value'].")
    parameter_value = parameter_info['Parameter']['Value']
    logger.info("Value found. Returning...")
    return parameter_value


def get_ssm_parameter_value_from_env(parameter_name):
    """Make a get request to SSM for the given parameter and return un-encrypted value"""
    parameter_env = get_environmental_variable_value(variable_name=parameter_name)
    parameter_value = get_ssm_parameter_value(parameter_name=parameter_env)
    return parameter_value

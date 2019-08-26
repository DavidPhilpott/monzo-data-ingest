import boto3
import os
import logging
import requests
import json
from datetime import date, timedelta


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


def build_job_trigger_message():
    """Create an SNS message for the core SNS to trigger Monzo data ingest jobs."""
    logger.info("Creating message for SNS to publish.")
    sns_message_attributes = {}
    sns_message_attributes["service"] = {
        "DataType": "String",
        "StringValue": "Monzo-Data-Ingest"}
    sns_message_attributes["date_to_process"] = {
        "DataType": "String",
        "StringValue": get_yesterdays_date()
    }
    logger.debug("Message attributes to be publish are: %s" % str(sns_message_attributes))
    logger.info("Message built.")
    return sns_message_attributes


def get_yesterdays_date():
    """Construct yesterday's date as a string in YYYY-MM-DD"""
    logger.info("Fetching yesterday's date as YYYY-MM-DD.")
    yesterday = date.today() - timedelta(days=1)
    yesterday_formatted = yesterday.strftime('%Y-%m-%d')
    logger.debug("Date obtained: '%s'." % yesterday_formatted)
    return yesterday_formatted


def publish_message_to_sns(sns_message_attributes, topic_arn):
    """Publish a message to a given SNS"""
    logger.info("Publishing message to SNS.")
    logger.debug("Creating SNS client.")
    sns_client = boto3.client('sns')
    logger.debug("About to publish message to topic: %s." % sns_message_attributes)
    response = sns_client.publish(TopicArn=topic_arn,
                                  Subject='Monzo-Data-Ingest Job Trigger',
                                  Message='', #json.dumps(sns_message_attributes),
                                  MessageAttributes=sns_message_attributes)
    logger.info("Message published. Returning.")
    return response


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

    logger.info("-- Publish Trigger Message to SNS --")
    message_to_publish = build_job_trigger_message()
    publish_response = publish_message_to_sns(sns_message_attributes=message_to_publish,
                                              topic_arn=sns_topic_arn)
    logger.debug("Publish response: %s." % publish_response)
    logger.info("Function finished.")
    return

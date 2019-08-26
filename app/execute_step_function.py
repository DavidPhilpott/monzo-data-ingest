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


def execute_step_function(step_function_arn, step_function_execution_name, input_values):
    """Call a step function arn with a given execution name and input"""
    logger.info("Starting step function execution '%s'." % step_function_execution_name)
    logger.debug("Step function ARN: %s." % step_function_arn)
    logger.debug("Step function input values:")
    logger.debug(input_values)
    logger.debug("Creating step function client.")
    step_function_client = boto3.client('stepfunctions')
    logger.debug("Calling execution.")
    response = step_function_client.start_execution(
        stateMachineArn=step_function_arn,
        name=step_function_execution_name,
        input=json.dumps(input_values)
    )
    logger.debug("Finished. Returning response...")
    return response


def extract_date_to_process_from_message(event_message):
    """Reach in to sns message (from lambda event) and extract the date_to_process value"""
    logger.info("Extracting date to process from lambda event.")
    job_message = json.loads(event_message['Records'][0]['body'])
    date_to_process = job_message['MessageAttributes']['date_to_process']['Value']
    logger.debug("Found value %s." % date_to_process)
    return date_to_process


def build_step_function_input_json(date_to_process):
    """Build input json for step function. Contains date identifying relevant data for this job."""
    logger.info("Building input json for step function.")
    input_dict = {}
    input_dict['date_to_process'] = date_to_process
    input_json = json.dumps(input_dict)
    logger.debug("Created string is: %s" % input_json)
    logger.info("Finished creating input json.")
    return input_json


def generate_execution_name(date_to_process):
    """Create a unique execution name for this job"""
    logger.info("Creating execution name.")
    current_time_string = date.today().strftime('%Y%m%d%H%M%S')
    execution_name = "Monzo-Data-Ingest-%s-%s" % (date_to_process, current_time_string)
    logger.debug("Execution name is '%s'" % execution_name)
    logger.info("Finished generating execution name.")
    return execution_name


def main(event, context):
    print("-- Instantiating logger --")
    global logger
    logger = logging.getLogger(__name__)
    logger.propagate = False
    set_logger_level(logger)
    set_logger_format(logger)

    logger.info("-- Getting Parameter Values --")
    target_step_function_arn = os.getenv('target_step_function_arn')
    logger.info("Finished getting parameter values.")

    logger.info("-- Getting Job Information --")
    date_to_process = extract_date_to_process_from_message(event_message=event)
    step_function_input = build_step_function_input_json(date_to_process=date_to_process)
    execution_name = generate_execution_name(date_to_process)
    logger.info("Finished getting job information.")

    logger.info("-- Executing Step Function --")
    execution_response = execute_step_function(step_function_arn=target_step_function_arn,
                                               step_function_execution_name=execution_name,
                                               input_values=step_function_input)
    logger.info("Function finished.")
    return

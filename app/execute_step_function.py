import boto3
import os
import logging
import logger_setup as logger_setup
import json
from datetime import datetime


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
    logger.info("Finished extracting date to process.")
    return date_to_process


def build_step_function_input_json(date_to_process):
    """Build input json for step function. Contains date identifying relevant data for this job."""
    logger.info("Building input json for step function.")
    input_string = '{"date_to_process": "%s"}' % date_to_process
    #input_dict = {}
    #input_dict['date_to_process'] = date_to_process
    #input_json = json.dumps(input_dict)
    logger.debug("Created string is: %s" % input_string)
    logger.info("Finished creating input json.")
    return input_string


def generate_execution_name(date_to_process):
    """Create a unique execution name for this job"""
    logger.info("Creating execution name.")
    current_time_string = datetime.now().strftime('%Y%m%d%H%M%S')
    execution_name = "Monzo-Data-Ingest-%s-%s" % (date_to_process, current_time_string)
    logger.debug("Execution name is '%s'" % execution_name)
    logger.info("Finished generating execution name.")
    return execution_name


def main(event, context):
    print("-- Instantiating logger --")
    global logger
    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger_setup.set_logger_level(logger)
    logger_setup.set_logger_format(logger)

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

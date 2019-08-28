import boto3
import os
import logging
import app.logger_setup as logger_setup
import app.aws_utilities as aws
import requests
import json


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
    logger_setup.set_logger_level(logger)
    logger_setup.set_logger_format(logger)

    logger.info("-- Getting Parameter Values --")
    access_key = aws.get_ssm_parameter_value(parameter_name='access_key_parameter')
    logger.info("Finished getting parameter values.")

    logger.info("-- Testing Current Access Keys --")
    if authorisation_test(access_key) is True:
        logger.info("Authorisation test PASSED. Keys do not need to be refreshed.")
        return {"auth_granted": "true"}
    else:
        logger.info("Authorisation test FAILED. Keys need to be refreshed.")
        return {"auth_granted": "false"}

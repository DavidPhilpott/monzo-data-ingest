import logging
import app.logger_setup as logger_setup
import app.utilities as aws
import requests
import json


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


def main(event, context):
    print("-- Instantiating logger --")
    global logger
    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger_setup.set_logger_level(logger)
    logger_setup.set_logger_format(logger)

    logger.info("-- Getting Parameter Values --")
    client_id = aws.get_ssm_parameter_value_from_env(parameter_name='client_id_parameter')
    client_secret_id = aws.get_ssm_parameter_value_from_env(parameter_name='client_secret_id_parameter')
    refresh_token = aws.get_ssm_parameter_value_from_env(parameter_name='refresh_token_parameter')
    logger.info("Finished getting parameter values.")
    logger.info("-- Getting New Access Tokens --")
    new_access_key, new_refresh_token = refresh_access_key(client_id=client_id,
                                                           client_secret_id=client_secret_id,
                                                           refresh_token=refresh_token)
    logger.info("Finished getting new access tokens.")
    logger.info("-- Writing New Tokens to SSM -- ")
    aws.write_ssm_parameter_value_from_env(parameter_name='access_key_parameter',
                                           new_parameter_value=new_access_key,
                                           is_secure=True)
    aws.write_ssm_parameter_value_from_env(parameter_name='refresh_token_parameter',
                                           new_parameter_value=new_refresh_token,
                                           is_secure=True)
    return

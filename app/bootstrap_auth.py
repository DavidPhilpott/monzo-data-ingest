import logging
import app.logger_setup as logger_setup
import app.utilities as aws
import requests

global logger
logger = logging.getLogger(__name__)
logger.propagate = False
logger_setup.set_logger_level(logger)
logger_setup.set_logger_format(logger)


def bootstrap_access_and_refresh_tokens(client_id, client_secret_id,
                                        redirect_uri, initial_access_code):
    """Make a request to the initial oauth monzo api. Exchange a bootstrap access code for an access key
    and a refresh token."""
    logger.info("Making request for tokens.")
    url = "https://api.monzo.com/oauth2/token"
    params = {"grant_type": "authorization_code",
              "client_id": client_id,
              "client_secret_id": client_secret_id,
              "redirect_uri": redirect_uri,
              "code": initial_access_code}
    logger.debug("Submitting request to %s." % url)
    response = requests.post(url, data=params)
    logger.debug("Received response.")
    logger.debug("Setting tokens as response.text.")
    tokens = response.text
    print(response.text)
    logger.debug("Returning tokens['access_token'], tokens['refresh_token'].")
    logger.info("Returning tokens.")
    return tokens['access_token'], tokens['refresh_token']


def main(event, context):
    logger.info("-- Getting Parameter Values --")
    monzo_bootstrap_token = aws.get_ssm_parameter_value_from_env(parameter_name='monzo_bootstrap_token_parameter')
    client_id = aws.get_ssm_parameter_value_from_env(parameter_name='client_id_parameter')
    client_secret_id = aws.get_ssm_parameter_value_from_env(parameter_name='client_secret_id_parameter')
    redirect_uri = aws.get_ssm_parameter_value_from_env(parameter_name='redirect_uri_parameter')
    logger.info("Finished getting parameter values.")
    logger.debug("Getting Monzo client.")

    logger.info("-- Requesting Bootstrap Access Tokens --")
    access_key, refresh_token = bootstrap_access_and_refresh_tokens(client_id=client_id,
                                                                    client_secret_id=client_secret_id,
                                                                    redirect_uri=redirect_uri,
                                                                    initial_access_code=monzo_bootstrap_token)
    logger.info("Got tokens.")
    logger.info("-- Writing Access Tokens to SSM --")
    aws.write_ssm_parameter_value_from_env(parameter_name='access_key_parameter',
                                           new_parameter_value=access_key,
                                           is_secure=True)
    aws.write_ssm_parameter_value_from_env(parameter_name='refresh_token_parameter',
                                           new_parameter_value=refresh_token,
                                           is_secure=True)
    logger.info("Finished writing to SSM.")
    return


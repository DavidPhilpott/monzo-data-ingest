logger.info("-- Refreshing Keys --")
new_access_key, new_refresh_token = refresh_access_key(client_id, client_secret_id, refresh_token)

access_key = get_ssm_parameter_value(parameter_name='access_key_parameter')
client_id = get_ssm_parameter_value(parameter_name='client_id_parameter')
client_secret_id = get_ssm_parameter_value(parameter_name='client_secret_id_parameter')
refresh_token = get_ssm_parameter_value(parameter_name='refresh_token_parameter')
redirect_uri = get_ssm_parameter_value(parameter_name='redirect_uri_parameter')

def refresh_access_key(client_id, client_secret_id, refresh_token):
    """Submit refresh token to monzo in echange for a new access key and refresh token"""
    logger.info("Exchanging refresh token with Monzo.")
    api_url = 'https://api.monzo.com/oauth2/token'
    refresh_params = {'grant_type': 'refresh_token',
                      'client_id': client_id,
                      'client_secret': client_secret_id,
                      'refresh_token': refresh_token}
    logging.debug("Submitting to '%s'" % api_url)
    #raw_result = requests.post(url=api_url, data=refresh_params)
    logging.debug("Received result. Parsing JSON.")
    #result = json.loads(raw_result.text)
    logging.debug("Returning access_token and refresh_token.")
    return "a", "b"#result['access_token'], result['refresh_token']


import requests
import json

TOKEN_FILE_PATH = "tokens.json"


class APIClient():
    """
    Wrapper object for making api calls use requests. Makes mocking out api calls in code easier.
    """
    def __init__(self):
        return

    def post(self, api_url: str, api_parameters: str):
        return requests.post(url=api_url, data=api_parameters)


def read_tokens(token_file_path):
    token_file = open(token_file_path, "r")
    token_contents = token_file.read()
    tokens = json.loads(token_contents)
    token_file.close()
    return tokens


def write_tokens(token_file_path, tokens_to_write):
    token_file = open(token_file_path, "w")
    token_file.write(json.dumps(tokens_to_write))
    token_file.close()
    return


def refresh_auth_token(api_client, client_id, client_secret, refresh_token):
    api_url = 'https://api.monzo.com/oauth2/token'
    refresh_params = {'grant_type': 'refresh_token',
                      'client_id': client_id,
                      'client_secret': client_secret,
                      'refresh_token': refresh_token}

    r = api_client.post(api_url=api_url, api_parameters=refresh_params)

    new_tokens = {'access_token': json.loads(r)['access_token'],
                  'refresh_token': json.loads(r)['refresh_token']}
    return new_tokens


def test_access(api_client, client_id, client_secret, access_token):
    api_url = 'https://api.monzo.com/oauth2/token'
    parameters = {'grant_type': 'authorization_code',
                  'client_id': client_id,
                  'client_secret': client_secret,
                  'redirect_uri': 'http://localhost:2020',
                  'code': access_token}
    r = api_client.post(api_url=api_url, api_parameters=parameters)
    result_test = r.text
    return result_test


api_client = APIClient()

token_set = read_tokens(token_file_path=TOKEN_FILE_PATH)
client_id = token_set['client_id']
client_secret = token_set['client_secret']
refresh_token = token_set['refresh_token']
access_token = token_set['access_token']


result_test = test_access(api_client=api_client,
                          client_id=client_id,
                          client_secret=client_secret,
                          access_token=access_token)
response_dict = json.loads(result_test)
if 'error' in response_dict.keys():
    if response_dict['code'] == 'unauthorized.bad_authorization_code.expired':
        new_tokens = refresh_auth_token(api_client=api_client,
                                        client_id=client_id,
                                        client_secret=client_secret,
                                        refresh_token=refresh_token)
        refresh_token = new_tokens['refresh_token']
        access_token = new_tokens['access_token']

        new_token_set = {'client_id': client_id,
                         'client_secret': client_secret,
                         'refresh_token': refresh_token,
                         'access_token': access_token}

        write_tokens(TOKEN_FILE_PATH, tokens_to_write=new_token_set)

print(response_dict["code"])
import requests
import json
from monzo import Monzo
import pandas as pd

TOKEN_FILE_PATH = "tokens.json"


class APIClient():
    """
    Wrapper object for making api calls use requests. Makes mocking out api calls in code easier.
    """
    def __init__(self):
        return

    def post(self, api_url: str, api_parameters: str):
        print([api_url, api_parameters])
        return requests.post(url=api_url, data=api_parameters)


def read_tokens(token_file_path: str) -> dict:
    """
    Read in the credential tokens and return them as a dict
    """
    token_file = open(token_file_path, "r")
    token_contents = token_file.read()
    tokens = json.loads(token_contents)
    token_file.close()
    return tokens


def write_tokens(token_file_path: str, tokens_to_write: dict) -> None:
    """
    Read in a dict of tokens and write them to a file
    """
    token_file = open(token_file_path, "w")
    token_file.write(json.dumps(tokens_to_write))
    token_file.close()
    return


def refresh_auth_token(api_client, token_set):
    client_id = token_set['client_id']
    client_secret = token_set['client_secret']
    refresh_token = token_set['refresh_token']
    api_url = 'https://api.monzo.com/oauth2/token'
    refresh_params = {'grant_type': 'refresh_token',
                      'client_id': client_id,
                      'client_secret': client_secret,
                      'refresh_token': refresh_token}

    r = api_client.post(api_url=api_url, api_parameters=refresh_params)

    new_tokens = {'access_key': json.loads(r)['access_token'],
                  'refresh_token': json.loads(r)['refresh_token']}
    return new_tokens


def test_valid_access_key(monzo_client):
    access_test = monzo_client.whoami()
    return access_test['authenticated']


token_set = read_tokens(token_file_path=TOKEN_FILE_PATH)
access_key = token_set['access_key']

monzo = Monzo(access_key)
if test_valid_access_key(monzo_client=monzo) is False:
    api_client = APIClient()
    new_tokens = refresh_auth_token(api_client=api_client,
                                    token_set=token_set)
    new_token_set = {'client_id': token_set['client_id'],
                     'client_secret': token_set['client_secret'],
                     'refresh_token': new_tokens['refresh_token'],
                     'access_key': new_tokens['access_key']}

    write_tokens(TOKEN_FILE_PATH, tokens_to_write=new_token_set)
    monzo = Monzo(access_key)

account_list = monzo.get_accounts()['accounts']
for account in account_list:
    if account['closed'] is False:
        account_id = account['id']
    print('id: %s, closed: %s' %(account['id'], account['closed']))

print(account_id)

balance = monzo.get_balance(account_id) # Get your balance object
print(balance['balance']) # 100000000000
print(balance['currency']) # GBP
print(balance['spend_today']) # 2000

transactions = monzo.get_transactions(account_id)
print(transactions)

pots = monzo.get_pots()['pots']
print(pots)
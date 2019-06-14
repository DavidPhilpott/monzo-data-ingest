import requests
import json


class AuthenticationHandler:
    def __init__(self):
        return

    @staticmethod
    def read_local_tokens(token_file_path: str) -> dict:
        """
        Read in the credential tokens and return them as a dict
        """
        token_file = open(token_file_path, "r")
        token_contents = token_file.read()
        tokens = json.loads(token_contents)
        token_file.close()
        return tokens

    @staticmethod
    def assemble_refresh_request_parameters(client_id: str, client_secret: str, refresh_token: str) -> dict:
        api_parameters = {"grant_type": "refresh_token", "client_id": client_id,
                          "client_secret": client_secret, "refresh_token": refresh_token}
        return api_parameters



    def get_new_auth_code(self):
        api_url = "https://api.monzo.com/oauth2/token"
        api_parameters = {"grant_type": "authorization_code",
                          "client_id": "oauth2client_00009jNbjw1TBhb75yrnlZ",
                          "client_secret": "",
                          "redirect_uri": "http://localhost:2020",
                          "code": ""}
        response = requests.post(url=api_url, data=api_parameters).text
        token_file = open("temp_tokens.txt", "w")
        token_file.write(json.dumps(response))
        token_file.close()
        return


class APIClient():
    """
    Wrapper object for making api calls use requests. Makes mocking out api calls in code easier.
    """
    def __init__(self):
        return

    def post(self, api_url: str, api_parameters: str):
        #print([api_url, api_parameters])
        return requests.post(url=api_url, data=api_parameters)


def get_new_tokens():
    url = "https://api.monzo.com/oauth2/token"
    params = {"grant_type": "authorization_code",
              "client_id": "oauth2client_00009jNbjw1TBhb75yrnlZ",
              "client_secret": "",
              "redirect_uri": "http://localhost:2020",
              "code": ""}
    request_client = APIClient()
    response = request_client.post(api_url=url, api_parameters=params).text
    token_file = open("temp_tokens.txt", "w")
    token_file.write(json.dumps(response))
    token_file.close()
    return
import mock
import os
import bootstrap_auth as bootstrap_auth
from moto import mock_ssm
import boto3


@mock.patch.dict(os.environ, {'logging_level': 'DEBUG'})
@mock_ssm
@mock.patch("app.bootstrap_auth.bootstrap_access_and_refresh_tokens")
def test_main_integration_correct_state(bootstrap_access_and_refresh_tokens_mock):
    """Integration test for main function. Provide correct setup and validate correct state"""

    bootstrap_access_and_refresh_tokens_mock.return_value = ["Test Access Key New Value", "Test Token New Value"]

    os.environ["monzo_bootstrap_token_parameter"] = "Test Bootstrap Token"
    os.environ["client_id_parameter"] = "Test Client ID"
    os.environ["client_secret_id_parameter"] = "Test Secret ID"
    os.environ["redirect_uri_parameter"] = "Test Redirect URI"
    os.environ["access_key_parameter"] = "Test Access Key"
    os.environ["refresh_token_parameter"] = "Test Refresh Token"

    virtual_ssm_client = boto3.client('ssm')
    virtual_ssm_client.put_parameter(Name="Test Bootstrap Token",
                                     Value="Test Bootstrap Value",
                                     Type="String",
                                     Overwrite=True)
    virtual_ssm_client.put_parameter(Name="Test Client ID",
                                     Value="Test Client ID Value",
                                     Type="String",
                                     Overwrite=True)
    virtual_ssm_client.put_parameter(Name="Test Secret ID",
                                     Value="Test Secret ID Value",
                                     Type="String",
                                     Overwrite=True)
    virtual_ssm_client.put_parameter(Name="Test Redirect URI",
                                     Value="Test Redirect URI Value",
                                     Type="String",
                                     Overwrite=True)
    virtual_ssm_client.put_parameter(Name="Test Access Key",
                                     Value="Test Access Key Base Value",
                                     Type="String",
                                     Overwrite=True)
    virtual_ssm_client.put_parameter(Name="Test Refresh Token",
                                     Value="Test Refresh Token Base Value",
                                     Type="String",
                                     Overwrite=True)

    bootstrap_auth.main("Event", "Context")

    virtual_access_key_ssm_value = virtual_ssm_client.get_parameters(
        Names=['Test Access Key'],
        WithDecryption=True
    )['Parameters'][0]['Value']
    virtual_refresh_token_ssm_value = virtual_ssm_client.get_parameters(
        Names=['Test Refresh Token'],
        WithDecryption=True
    )['Parameters'][0]['Value']

    assert virtual_access_key_ssm_value == "Test Access Key New Value" and \
           virtual_refresh_token_ssm_value == "Test Token New Value"
    return


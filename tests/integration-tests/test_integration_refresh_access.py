import app.refresh_access as refresh_access
from moto import mock_ssm
import boto3
import mock
import os


@mock_ssm
@mock.patch.dict(os.environ, {'logging_level': 'DEBUG'})
@mock.patch("app.refresh_access.refresh_access_key")
def test_refresh_access_passes(mocked_refresh_access_key):
    """Validate that new refresh keys are correctly written to SSM"""
    virtual_ssm_client = boto3.client('ssm')
    virtual_ssm_client.put_parameter(Name="Test Client ID",
                                     Value="Test Client ID",
                                     Type="String",
                                     Overwrite=True)
    virtual_ssm_client.put_parameter(Name="Test Secret ID",
                                     Value="Test Secret ID",
                                     Type="String",
                                     Overwrite=True)
    virtual_ssm_client.put_parameter(Name="Test Refresh Token",
                                     Value="Test Refresh Token Param",
                                     Type="SecureString",
                                     Overwrite=True)
    virtual_ssm_client.put_parameter(Name="Test Access Key",
                                     Value="Test Access Key",
                                     Type="SecureString",
                                     Overwrite=True)
    os.environ["refresh_token_parameter"] = "Test Refresh Token"
    os.environ["client_id_parameter"] = "Test Client ID"
    os.environ["client_secret_id_parameter"] = "Test Secret ID"
    os.environ["access_key_parameter"] = "Test Access Key"
    mocked_refresh_access_key.return_value = ("Valid Access Key", "Valid Refresh Token")

    refresh_access.main("Test Event", "Test Context")
    output_access_key_ssm_value = virtual_ssm_client.get_parameters(
        Names=['Test Access Key'],
        WithDecryption=True
    )['Parameters'][0]['Value']
    output_refresh_token_ssm_value = virtual_ssm_client.get_parameters(
        Names=['Test Refresh Token'],
        WithDecryption=True
    )['Parameters'][0]['Value']
    assert output_access_key_ssm_value == 'Valid Access Key'
    assert output_refresh_token_ssm_value == 'Valid Refresh Token'
    return

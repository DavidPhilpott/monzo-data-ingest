import mock
import os
import app.ingest_data_accounts as ingest_data_accounts
from moto import mock_ssm, mock_s3
import boto3
import json


@mock.patch.dict(os.environ, {'logging_level': 'DEBUG'})
@mock_ssm
@mock_s3
@mock.patch("app.ingest_data_accounts.get_account_data")
def test_ingest_data_accounts_passes(mocked_get_account_data):
    """Integration test for main function - mock out process for receiving data and validate final state"""
#   set up virtual bucket
    virtual_client = boto3.client("s3")
    test_bucket_name = 'Test_Bucket'
    virtual_client.create_bucket(Bucket=test_bucket_name)
#   set up access key SSM
    virtual_ssm_client = boto3.client('ssm')
    virtual_ssm_client.put_parameter(Name="Test Access Key",
                                     Value="Test Access Key Base Value",
                                     Type="String",
                                     Overwrite=True)
#   Set env vars
    os.environ["access_key_parameter"] = "Test Access Key"
    os.environ["data_lake_bucket_name"] = test_bucket_name
    os.environ["environment"] = "Int_Test"
#   mock Monzo return with valid data
    test_account_data = {"accounts": "123456"}
    mocked_get_account_data.return_value = test_account_data
#   set batch id via event
    test_event = {"date_to_process": "1990-01-01"}
#   run main
    ingest_data_accounts.main(event=test_event, context="Context")
#   seek data from virtual s3
    virtual_resource_client = boto3.resource("s3")
    expected_path = "monzo/Int_Test/1990-01-01/account-data.json"
    output_object = virtual_resource_client.Object(test_bucket_name, expected_path)
    test_output_data = output_object.get()['Body'].read().decode('utf-8')
    assert str(test_output_data) == json.dumps(test_account_data)
    return






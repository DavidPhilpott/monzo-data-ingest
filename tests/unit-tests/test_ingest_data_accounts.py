import app.ingest_data_accounts as ingest_data_accounts
import mock
from moto import mock_s3
import boto3


@mock.patch("monzo.Monzo")
def test_get_monzo_client_pass(mocked_monzo):
    valid_output = "Test"
    mocked_monzo.return_value = valid_output
    test_output = ingest_data_accounts.get_monzo_client(access_key="123")
    assert str(test_output.__class__) == "<class 'monzo.monzo.Monzo'>"
    return


def test_get_account_data_pass():
    """Test that account information is pulled from Monzo client response"""
    mock_client = mock.Mock()
    test_account_data = "Test Data"
    mock_client.get_accounts.return_value = test_account_data
    test_output = ingest_data_accounts.get_account_data(monzo_client=mock_client)
    assert test_output == test_account_data
    return


def test_get_account_list_pass():
    """Test that account list data extracts from account_data"""
    valid_output = "Test Data"
    mock_data = {"accounts": valid_output}
    test_output = ingest_data_accounts.get_account_list(account_data=mock_data)
    assert test_output == valid_output
    return


def test_build_data_lake_target_path_pass():
    """Test that the correct path is built for given input"""
    mock_project = "Test_Project"
    mock_env = "Test_Env"
    mock_date = "YYYY-MM-DD"
    mock_filename = "Test_Name"
    valid_output = mock_project + "/" + mock_env + "/" + mock_date + "/" + mock_filename
    test_output = ingest_data_accounts.build_data_lake_target_path(project=mock_project,
                                                                   environment=mock_env,
                                                                   date=mock_date,
                                                                   filename=mock_filename)
    assert test_output == valid_output
    return


@mock_s3
def test_get_s3_client():
    """Test wrapper for s3 client"""
    test_output = ingest_data_accounts.get_s3_client()
    assert str(test_output.__class__) == "<class 'botocore.client.S3'>"
    return


@mock_s3
def test_write_data_to_s3():
    """Test file is correctly written to S3"""
    virtual_client = boto3.client("s3")
    test_bucket_name = 'Test_Bucket'
    test_target_path = 'TestPath'
    test_data_to_write = 'TestData'
    virtual_client.create_bucket(Bucket=test_bucket_name)
    ingest_data_accounts.write_data_to_s3(s3_client=virtual_client,
                                          bucket_name=test_bucket_name,
                                          target_path=test_target_path,
                                          data_to_write=test_data_to_write)
    virtual_resource_client = boto3.resource('s3')
    output_object = virtual_resource_client.Object(test_bucket_name, test_target_path)
    test_output_data = output_object.get()['Body'].read().decode('utf-8')
    assert test_output_data == test_data_to_write
    return

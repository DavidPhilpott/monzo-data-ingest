import boto3
from moto import mock_ssm
from app.utilities import write_ssm_parameter_value, write_ssm_parameter_value_from_env, get_ssm_parameter_value_from_env
import mock
import os


@mock_ssm
def test_write_ssm_parameter_value_unsecure_successful_name():
    """pass valid input for writing unsecure string - expect to be able to find parameter by name"""
    test_name = "test_unsecured_param"
    test_value = "test value"
    is_secure = False
    write_ssm_parameter_value(parameter_name=test_name,
                              new_parameter_value=test_value,
                              is_secure=is_secure)
    virtual_ssm_client = boto3.client('ssm')
    response = virtual_ssm_client.get_parameters(
        Names=[test_name],
        WithDecryption=False
    )
    assert response['Parameters'][0]['Name'] == test_name
    return


@mock_ssm
def test_write_ssm_parameter_value_unsecure_successful_value():
    """pass valid input for writing unsecure string - expect to be able to find parameter value"""
    test_name = "test_unsecured_param"
    test_value = "test value"
    is_secure = False
    write_ssm_parameter_value(parameter_name=test_name,
                              new_parameter_value=test_value,
                              is_secure=is_secure)
    virtual_ssm_client = boto3.client('ssm')
    response = virtual_ssm_client.get_parameters(
        Names=[test_name],
        WithDecryption=False
    )
    assert response['Parameters'][0]['Value'] == test_value
    return


@mock_ssm
def test_write_ssm_parameter_value_secure_successful_name():
    """pass valid input for writing secure string - expect to be able to find parameter by name"""
    test_name = "test_unsecured_param"
    test_value = "test value"
    is_secure = True
    write_ssm_parameter_value(parameter_name=test_name,
                              new_parameter_value=test_value,
                              is_secure=is_secure)
    virtual_ssm_client = boto3.client('ssm')
    response = virtual_ssm_client.get_parameters(
        Names=[test_name],
        WithDecryption=True
    )
    assert response['Parameters'][0]['Name'] == test_name
    return


@mock_ssm
def test_write_ssm_parameter_value_secure_successful_value():
    """pass valid input for writing secure string - expect to be able to find and decrypt parameter value"""
    test_name = "test_unsecured_param"
    test_value = "test value"
    is_secure = True
    write_ssm_parameter_value(parameter_name=test_name,
                              new_parameter_value=test_value,
                              is_secure=is_secure)
    virtual_ssm_client = boto3.client('ssm')
    response = virtual_ssm_client.get_parameters(
        Names=[test_name],
        WithDecryption=True
    )
    assert response['Parameters'][0]['Value'] == test_value
    return


@mock_ssm
def test_write_ssm_parameter_value_secure_successful_value_encrypted():
    """pass valid input for writing secure string - expect to not be able to read value without decryption"""
    test_name = "test_unsecured_param"
    test_value = "test value"
    is_secure = True
    write_ssm_parameter_value(parameter_name=test_name,
                              new_parameter_value=test_value,
                              is_secure=is_secure)
    virtual_ssm_client = boto3.client('ssm')
    response = virtual_ssm_client.get_parameters(
        Names=[test_name],
        WithDecryption=False
    )
    assert response['Parameters'][0]['Value'] != test_value
    return


@mock_ssm
@mock.patch.dict(os.environ, {'test_parameter_env_ref': 'test_env_param_name'})
def test_write_ssm_parameter_value_from_env_successful_write():
    """Call function with an env variable set - should be able to get back value after write"""
    test_name = "test_parameter_env_ref"
    test_value = "test value"
    is_secure = False

    write_ssm_parameter_value_from_env(parameter_name=test_name,
                                       new_parameter_value=test_value,
                                       is_secure=is_secure)
    virtual_ssm_client = boto3.client('ssm')
    response = virtual_ssm_client.get_parameters(
        Names=['test_env_param_name'],
        WithDecryption=False
    )
    assert response['Parameters'][0]['Name'] == 'test_env_param_name'
    return
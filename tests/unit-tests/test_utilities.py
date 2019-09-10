import boto3
from moto import mock_ssm
from app.utilities import \
    write_ssm_parameter_value,\
    write_ssm_parameter_value_from_env,\
    get_ssm_parameter_value_from_env,\
    get_ssm_parameter_value,\
    get_environmental_variable_value
import mock
import os
import pytest


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


@mock_ssm
@mock.patch.dict(os.environ, {'test_parameter_env_ref': 'test_env_param_name'})
def test_get_ssm_parameter_value_from_env_write_value_and_retrieve():
    """Write a value to SSM and then retrive the value via OS env"""
    test_value = 'test_value'
    virtual_ssm_client = boto3.client('ssm')
    virtual_ssm_client.put_parameter(Name='test_env_param_name',
                                     Value=test_value,
                                     Type='String',
                                     Overwrite=True)
    test_parameter_name = 'test_parameter_env_ref'
    value = get_ssm_parameter_value_from_env(parameter_name=test_parameter_name)
    assert value == test_value
    return


@mock_ssm
def test_get_ssm_parameter_value_unsecure_success():
    """Test that an unencrypted variable value can be retrieved from SSM"""
    test_parameter_name = "Test Name"
    test_parameter_value = "Test Value"
    virtual_ssm_client = boto3.client('ssm')
    virtual_ssm_client.put_parameter(Name=test_parameter_name,
                                     Value=test_parameter_value,
                                     Type='String',
                                     Overwrite=True)
    result = get_ssm_parameter_value(parameter_name=test_parameter_name)
    assert result == test_parameter_value
    return


@mock_ssm
def test_get_ssm_parameter_value_secure_success():
    """Test that an unencrypted variable value can be retrieved from SSM"""
    test_parameter_name = "Test Name"
    test_parameter_value = "Test Value"
    virtual_ssm_client = boto3.client('ssm')
    virtual_ssm_client.put_parameter(Name=test_parameter_name,
                                     Value=test_parameter_value,
                                     Type='SecureString',
                                     Overwrite=True)
    result = get_ssm_parameter_value(parameter_name=test_parameter_name)
    assert result == test_parameter_value
    return


@mock.patch.dict(os.environ, {'test name': 'test value'})
def test_get_environmental_variable_value_success():
    """Attempt to find an existing env variable - should get value"""
    test_param_name = 'test name'
    test_param_value = 'test value'
    result = get_environmental_variable_value(variable_name=test_param_name)
    assert result == test_param_value
    return


def test_get_environmental_variable_value_fail_get_value_error():
    """Attempt to find a non-existent variable - should get error specifying attempted variable name"""
    test_param_name = 'test_variable'
    with pytest.raises(ValueError, match="Could not find value for environmental variable 'test_variable'."):
        get_environmental_variable_value(variable_name=test_param_name)
    return

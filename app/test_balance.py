from balance import valid_access_key
import unittest.mock as mock


def test_test_valid_access_key_returns_dict_with_authentication_key():
    monzo = mock.Mock()
    monzo.whoami.return_value = {'authenticated': 'Test Result'}
    assert valid_access_key(monzo_client=monzo) == 'Test Result'

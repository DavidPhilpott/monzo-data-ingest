import balance
from unittest.mock import Mock


def test_test_valid_access_key_returns_dict_with_authentication_key():
    monzo = Mock()
    monzo.whoami = {'Authentication': 'Test Result'}
    assert balance.test_valid_access_key(monzo_client=monzo) == 'Test Result'

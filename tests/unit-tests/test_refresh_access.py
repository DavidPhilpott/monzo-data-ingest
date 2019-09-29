import app.refresh_access as refresh_access
import mock
import json


@mock.patch("requests.post")
def test_refresh_access_key(mocked_request):
    """Pass in parameters and trigger return of new access keys and tokens"""
    test_client_id = "Test Client ID"
    test_client_secret_id = "Test Secret ID"
    test_refresh_token = "Test Refresh Token"
    valid_refresh_token = "Valid Refresh Token"
    valid_access_token = "Valid Access Key"
    mock_monzo_result = mock.Mock()
    test_data_set = json.dumps({'access_token': valid_access_token,
                                'refresh_token': valid_refresh_token})
    mock_monzo_result.text = test_data_set
    mocked_request.return_value = mock_monzo_result
    test_output_access, test_output_refresh = refresh_access.refresh_access_key(client_id=test_client_id,
                                                                                client_secret_id=test_client_secret_id,
                                                                                refresh_token=test_refresh_token)
    assert test_output_access == valid_access_token
    assert test_output_refresh == valid_refresh_token
    return

import mock
import app.bootstrap_auth as bootstrap_auth


@mock.patch("requests.post")
def test_bootstrap_access_and_refresh_tokens_pass_valid_success(mock_requests):
    """Test that passing valid parameters to the API returns desired result"""

    mock_response = mock.Mock()
    mock_response.text = {'access_token': 'valid access token', 'refresh_token': 'valid refresh token'}
    mock_requests.return_value = mock_response

    test_client_id = "Dummy ID"
    test_client_secret = "Dummy Secret"
    test_redirect_uri = "http://dummy.uri"
    test_initial_access_code = "Test Code"

    access, refresh = bootstrap_auth.bootstrap_access_and_refresh_tokens(client_id=test_client_id,
                                                                         client_secret_id=test_client_secret,
                                                                         redirect_uri=test_redirect_uri,
                                                                         initial_access_code=test_initial_access_code)
    assert access == 'valid access token' and refresh == 'valid refresh token'
    return

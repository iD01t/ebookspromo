from unittest import mock
from app import x_client

@mock.patch("builtins.print")
def test_post_tweet_success(mock_print):
    # Arrange
    message = "Test tweet"
    api_key = "test_key"
    api_secret = "test_secret"
    access_token = "test_token"
    access_token_secret = "test_token_secret"

    # Act
    result = x_client.post_tweet(message, api_key, api_secret, access_token, access_token_secret)

    # Assert
    assert result["status"] == "success"
    mock_print.assert_any_call(f"Message: {message}")

@mock.patch("builtins.print")
def test_post_tweet_no_credentials(mock_print):
    # Arrange
    message = "Test tweet"

    # Act
    result = x_client.post_tweet(message, "", "", "", "")

    # Assert
    assert result["status"] == "error"
    mock_print.assert_called_with("[WARNING] X API credentials are not set. Tweet was not sent.")

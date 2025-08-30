from unittest import mock
import pytest
import requests
from app.google_books_client import fetch_books_by_author

@mock.patch("requests.get")
def test_fetch_books_by_author_success(mock_get):
    # Arrange
    mock_response = mock.Mock()
    mock_response.json.return_value = {"items": [{"title": "Test Book"}]}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    author_name = "Test Author"
    api_key = "test_key"

    # Act
    books = fetch_books_by_author(author_name, api_key)

    # Assert
    assert books == [{"title": "Test Book"}]
    mock_get.assert_called_once()

@mock.patch("requests.get")
def test_fetch_books_by_author_request_exception(mock_get):
    # Arrange
    mock_get.side_effect = requests.exceptions.RequestException("Test error")

    author_name = "Test Author"
    api_key = "test_key"

    # Act
    books = fetch_books_by_author(author_name, api_key)

    # Assert
    assert books == []

def test_fetch_books_by_author_no_api_key():
    # Act
    books = fetch_books_by_author("Test Author", "")

    # Assert
    assert books == []

import os
from unittest import mock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Growth OS API is running."}

def test_launch_endpoint():
    response = client.post("/launch", json={"titles": ["Book 1", "Book 2"]})
    assert response.status_code == 200
    assert response.json() == {"message": "Launch wave initiated in the background."}

@mock.patch("app.storage.save_books")
@mock.patch("app.google_books_client.fetch_books_by_author")
def test_ingest_google_books_endpoint(mock_fetch_books, mock_save_books):
    # Arrange
    os.environ["GOOGLE_BOOKS_API_KEY"] = "test_key"
    mock_fetch_books.return_value = [{"title": "Test Book"}]
    author_name = "Test Author"

    # Act
    response = client.post("/ingest/google-books", json={"author_name": author_name})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Successfully ingested 1 books by '{author_name}'."}
    mock_fetch_books.assert_called_once_with(author_name, "test_key")
    mock_save_books.assert_called_once_with([{"title": "Test Book"}])

    # Clean up
    del os.environ["GOOGLE_BOOKS_API_KEY"]

def test_ingest_google_books_endpoint_no_api_key():
    # Act
    response = client.post("/ingest/google-books", json={"author_name": "Test Author"})

    # Assert
    assert response.status_code == 500
    assert response.json() == {"detail": "GOOGLE_BOOKS_API_KEY environment variable not set."}

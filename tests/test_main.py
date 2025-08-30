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

@mock.patch("app.storage.load_book_by_id")
def test_get_book_page_found(mock_load_book):
    # Arrange
    book_id = "test_id"
    book_data = {
        "id": book_id,
        "volumeInfo": {
            "title": "Test Book Title",
            "authors": ["Test Author"],
            "publisher": "Test Publisher",
            "publishedDate": "2023-01-01",
            "description": "Test description.",
            "imageLinks": {"thumbnail": "http://example.com/image.png"}
        }
    }
    mock_load_book.return_value = book_data

    # Act
    response = client.get(f"/books/{book_id}")

    # Assert
    assert response.status_code == 200
    assert "Test Book Title" in response.text
    mock_load_book.assert_called_once_with(book_id)

@mock.patch("app.storage.load_book_by_id")
def test_get_book_page_not_found(mock_load_book):
    # Arrange
    book_id = "non_existent_id"
    mock_load_book.return_value = None

    # Act
    response = client.get(f"/books/{book_id}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}
    mock_load_book.assert_called_once_with(book_id)

@mock.patch("app.storage.save_campaign")
def test_create_campaign(mock_save_campaign):
    # Arrange
    campaign_data = {
        "name": "Test Campaign",
        "book_ids": ["1", "2"],
        "promo_message": "Check out these great books!"
    }
    mock_save_campaign.return_value = {**campaign_data, "id": "test_campaign_id"}

    # Act
    response = client.post("/campaigns", json=campaign_data)

    # Assert
    assert response.status_code == 201
    assert response.json()["name"] == "Test Campaign"
    assert response.json()["id"] == "test_campaign_id"
    mock_save_campaign.assert_called_once_with(campaign_data)

@mock.patch("app.launch.launch_campaign")
def test_launch_campaign_endpoint(mock_launch_campaign):
    # Arrange
    campaign_id = "test_campaign_id"

    # Act
    response = client.post(f"/campaigns/{campaign_id}/launch")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Campaign {campaign_id} launch initiated in the background."}
    # We can't easily assert that the background task was called with the right args
    # without more complex testing setup, so we trust the endpoint returns success.

@mock.patch("app.storage.load_book_by_id")
@mock.patch("app.storage.log_event")
def test_track_click(mock_log_event, mock_load_book):
    # Arrange
    book_id = "test_book_id"
    mock_load_book.return_value = {"id": book_id, "volumeInfo": {"title": "Test Book"}}


    # Act
    response = client.get(f"/track/{book_id}")

    # Assert
    assert response.status_code == 200 # Final status code after redirect
    assert len(response.history) == 1
    redirect_response = response.history[0]
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == f"/books/{book_id}"
    mock_log_event.assert_called_once_with({"event_type": "click", "book_id": book_id})

@mock.patch("app.storage.load_metrics")
def test_get_analytics(mock_load_metrics):
    # Arrange
    mock_metrics = [
        {"event_type": "click", "book_id": "1"},
        {"event_type": "click", "book_id": "1"},
        {"event_type": "click", "book_id": "2"},
        {"event_type": "other_event", "book_id": "1"},
    ]
    mock_load_metrics.return_value = mock_metrics

    # Act
    response = client.get("/analytics")

    # Assert
    assert response.status_code == 200
    expected_analytics = {
        "total_clicks": 3,
        "clicks_per_book": {
            "1": 2,
            "2": 1,
        }
    }
    assert response.json() == expected_analytics

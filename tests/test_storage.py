import os
import json
from app import storage

def test_save_and_load_books(tmp_path):
    # Arrange
    storage.BOOKS_FILE = tmp_path / "test_books.json"
    books_to_save = [
        {"id": "1", "volumeInfo": {"title": "Book 1"}},
        {"id": "2", "volumeInfo": {"title": "Book 2"}},
    ]

    # Act
    storage.save_books(books_to_save)
    loaded_books = storage.load_books()

    # Assert
    assert len(loaded_books) == 2
    assert loaded_books["1"]["volumeInfo"]["title"] == "Book 1"

    # Act: Save more books to test merging
    more_books_to_save = [
        {"id": "3", "volumeInfo": {"title": "Book 3"}},
        {"id": "1", "volumeInfo": {"title": "Book 1 Updated"}}, # Test update
    ]
    storage.save_books(more_books_to_save)
    loaded_books = storage.load_books()

    # Assert
    assert len(loaded_books) == 3
    assert loaded_books["1"]["volumeInfo"]["title"] == "Book 1 Updated"


def test_load_book_by_id(tmp_path):
    # Arrange
    storage.BOOKS_FILE = tmp_path / "test_books.json"
    books_to_save = {
        "1": {"id": "1", "volumeInfo": {"title": "Book 1"}},
        "2": {"id": "2", "volumeInfo": {"title": "Book 2"}},
    }
    with open(storage.BOOKS_FILE, "w") as f:
        json.dump(books_to_save, f)

    # Act
    book1 = storage.load_book_by_id("1")
    book3 = storage.load_book_by_id("3")

    # Assert
    assert book1 is not None
    assert book1["volumeInfo"]["title"] == "Book 1"
    assert book3 is None

def test_load_books_file_not_found(tmp_path):
    # Arrange
    storage.BOOKS_FILE = tmp_path / "non_existent_file.json"

    # Act
    loaded_books = storage.load_books()

    # Assert
    assert loaded_books == {}

def test_save_and_load_campaigns(tmp_path):
    # Arrange
    storage.CAMPAIGNS_FILE = tmp_path / "test_campaigns.json"
    campaign_data = {
        "name": "Test Campaign",
        "book_ids": ["1", "2"],
        "promo_message": "Check out these great books!"
    }

    # Act
    new_campaign = storage.save_campaign(campaign_data)
    loaded_campaigns = storage.load_campaigns()

    # Assert
    assert len(loaded_campaigns) == 1
    campaign_id = new_campaign["id"]
    assert loaded_campaigns[campaign_id]["name"] == "Test Campaign"

def test_load_campaign_by_id(tmp_path):
    # Arrange
    storage.CAMPAIGNS_FILE = tmp_path / "test_campaigns.json"
    campaigns_to_save = {
        "test_id_1": {"id": "test_id_1", "name": "Campaign 1"},
        "test_id_2": {"id": "test_id_2", "name": "Campaign 2"},
    }
    with open(storage.CAMPAIGNS_FILE, "w") as f:
        json.dump(campaigns_to_save, f)

    # Act
    campaign1 = storage.load_campaign_by_id("test_id_1")
    campaign3 = storage.load_campaign_by_id("test_id_3")

    # Assert
    assert campaign1 is not None
    assert campaign1["name"] == "Campaign 1"
    assert campaign3 is None

def test_load_campaigns_file_not_found(tmp_path):
    # Arrange
    storage.CAMPAIGNS_FILE = tmp_path / "non_existent_file.json"

    # Act
    loaded_campaigns = storage.load_campaigns()

    # Assert
    assert loaded_campaigns == {}

def test_log_event_and_load_metrics(tmp_path):
    # Arrange
    storage.METRICS_FILE = tmp_path / "test_metrics.json"
    event1 = {"event_type": "click", "book_id": "1"}
    event2 = {"event_type": "click", "book_id": "2"}

    # Act
    storage.log_event(event1)
    storage.log_event(event2)
    loaded_metrics = storage.load_metrics()

    # Assert
    assert len(loaded_metrics) == 2
    assert loaded_metrics[0]["event_type"] == "click"
    assert "timestamp" in loaded_metrics[0]

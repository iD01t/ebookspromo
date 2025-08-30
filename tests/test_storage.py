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

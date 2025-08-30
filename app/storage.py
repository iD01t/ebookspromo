import json
from typing import List, Dict, Any, Optional
import os

DATA_DIR = "data"
BOOKS_FILE = os.path.join(DATA_DIR, "books.json")

def save_books(books: List[Dict[str, Any]]):
    """
    Saves a list of books to a JSON file, indexed by book ID.
    It merges the new books with existing ones.

    Args:
        books: A list of book data dictionaries from the Google Books API.
    """
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        existing_books = load_books()
        for book in books:
            book_id = book.get("id")
            if book_id:
                existing_books[book_id] = book

        with open(BOOKS_FILE, "w") as f:
            json.dump(existing_books, f, indent=4)
        print(f"[INFO] Successfully saved/updated {len(books)} books in {BOOKS_FILE}")
    except IOError as e:
        print(f"[ERROR] An error occurred while saving books to {BOOKS_FILE}: {e}")

def load_books() -> Dict[str, Any]:
    """
    Loads a dictionary of books from a JSON file.

    Returns:
        A dictionary of book data, with book IDs as keys.
    """
    try:
        if not os.path.exists(BOOKS_FILE):
            return {}

        with open(BOOKS_FILE, "r") as f:
            content = f.read()
            if not content:
                return {}
            return json.loads(content)
    except (IOError, json.JSONDecodeError) as e:
        print(f"[ERROR] An error occurred while loading books from {BOOKS_FILE}: {e}")
        return {}

def load_book_by_id(book_id: str) -> Optional[Dict[str, Any]]:
    """
    Loads a single book by its ID from the JSON file.

    Args:
        book_id: The ID of the book to retrieve.

    Returns:
        A dictionary of book data, or None if the book is not found.
    """
    books = load_books()
    return books.get(book_id)

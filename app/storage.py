import json
from typing import List, Dict, Any
import os

DATA_DIR = "data"
BOOKS_FILE = os.path.join(DATA_DIR, "books.json")

def save_books(books: List[Dict[str, Any]]):
    """
    Saves a list of books to a JSON file.

    Args:
        books: A list of book data dictionaries.
    """
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        with open(BOOKS_FILE, "w") as f:
            json.dump(books, f, indent=4)
        print(f"[INFO] Successfully saved {len(books)} books to {BOOKS_FILE}")
    except IOError as e:
        print(f"[ERROR] An error occurred while saving books to {BOOKS_FILE}: {e}")

def load_books() -> List[Dict[str, Any]]:
    """
    Loads a list of books from a JSON file.

    Returns:
        A list of book data dictionaries, or an empty list if the file doesn't exist or an error occurs.
    """
    try:
        if not os.path.exists(BOOKS_FILE):
            return []

        with open(BOOKS_FILE, "r") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"[ERROR] An error occurred while loading books from {BOOKS_FILE}: {e}")
        return []

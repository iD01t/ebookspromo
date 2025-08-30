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

# ==== Campaign Storage ====

import uuid

CAMPAIGNS_FILE = os.path.join(DATA_DIR, "campaigns.json")

def save_campaign(campaign_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Saves a new campaign to the campaigns file.

    Args:
        campaign_data: A dictionary containing the campaign details.

    Returns:
        The full campaign data, including its new ID.
    """
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        campaigns = load_campaigns()

        campaign_id = str(uuid.uuid4())
        campaign_data["id"] = campaign_id
        campaigns[campaign_id] = campaign_data

        with open(CAMPAIGNS_FILE, "w") as f:
            json.dump(campaigns, f, indent=4)

        print(f"[INFO] Successfully saved campaign {campaign_id} to {CAMPAIGNS_FILE}")
        return campaign_data
    except IOError as e:
        print(f"[ERROR] An error occurred while saving campaign to {CAMPAIGNS_FILE}: {e}")
        return None

def load_campaigns() -> Dict[str, Any]:
    """
    Loads a dictionary of campaigns from a JSON file.

    Returns:
        A dictionary of campaign data, with campaign IDs as keys.
    """
    try:
        if not os.path.exists(CAMPAIGNS_FILE):
            return {}

        with open(CAMPAIGNS_FILE, "r") as f:
            content = f.read()
            if not content:
                return {}
            return json.loads(content)
    except (IOError, json.JSONDecodeError) as e:
        print(f"[ERROR] An error occurred while loading campaigns from {CAMPAIGains_FILE}: {e}")
        return {}

def load_campaign_by_id(campaign_id: str) -> Optional[Dict[str, Any]]:
    """
    Loads a single campaign by its ID from the JSON file.

    Args:
        campaign_id: The ID of the campaign to retrieve.

    Returns:
        A dictionary of campaign data, or None if the campaign is not found.
    """
    campaigns = load_campaigns()
    return campaigns.get(campaign_id)

# ==== Analytics Storage ====

from datetime import datetime, timezone

METRICS_FILE = os.path.join(DATA_DIR, "metrics.json")

def log_event(event_data: Dict[str, Any]):
    """
    Logs a new event to the metrics file.

    Args:
        event_data: A dictionary containing the event details.
    """
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        metrics = load_metrics()

        event_data["timestamp"] = datetime.now(timezone.utc).isoformat()
        metrics.append(event_data)

        with open(METRICS_FILE, "w") as f:
            json.dump(metrics, f, indent=4)

        print(f"[INFO] Successfully logged event: {event_data['event_type']}")
    except IOError as e:
        print(f"[ERROR] An error occurred while logging event to {METRICS_FILE}: {e}")

def load_metrics() -> List[Dict[str, Any]]:
    """
    Loads a list of metric events from a JSON file.

    Returns:
        A list of event data dictionaries.
    """
    try:
        if not os.path.exists(METRICS_FILE):
            return []

        with open(METRICS_FILE, "r") as f:
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except (IOError, json.JSONDecodeError) as e:
        print(f"[ERROR] An error occurred while loading metrics from {METRICS_FILE}: {e}")
        return []

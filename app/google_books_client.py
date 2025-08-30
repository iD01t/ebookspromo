import requests
from typing import List, Dict, Any

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

def fetch_books_by_author(author_name: str, api_key: str) -> List[Dict[str, Any]]:
    """
    Fetches a list of books for a given author from the Google Books API.

    Args:
        author_name: The name of the author to search for.
        api_key: The Google Books API key.

    Returns:
        A list of book data dictionaries, or an empty list if an error occurs.
    """
    if not api_key:
        print("[ERROR] Google Books API key is not provided.")
        return []

    params = {
        "q": f"inauthor:{author_name}",
        "key": api_key,
        "maxResults": 40  # Fetch the maximum number of results per page
    }

    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data.get("items", [])
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] An error occurred while calling the Google Books API: {e}")
        return []
    except ValueError:
        print("[ERROR] Could not decode the response from the Google Books API.")
        return []

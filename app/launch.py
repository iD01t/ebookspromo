# launch.py
# Author: Guillaume Lessard (DJ iD01t)
# Goal: Automate a strategic launch wave for 250+ eBooks now available in Europe
# This script prepares and executes multi-channel distribution + indexing

import os
import requests
from datetime import datetime
from typing import List

# ==== CONFIGURATION ====
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BOOKS_CATALOG_URL = "https://play.google.com/store/books/author?id=DJ+iD01t"
LANDING_PAGE_URL = "https://id01t.eu"  # Replace with your real central link
SHORT_DESC = "Discover 250+ visionary eBooks now available across Europe."
LAUNCH_HASHTAGS = "#ebooks #GoogleBooks #AI #Europe #DJiD01t #RA7 #coding"

# === PRIMARY HOOKS ===

def ping_indexing_signal(title: str, url: str):
    """Fake trigger to simulate URL indexing (playbooks and click-throughs)."""
    print(f"Indexing signal triggered for: {title}")
    # Can be extended to hit analytics endpoints or click simulators


def post_gemini_blast(title: str, content: str, image_url: str = None):
    """Send a Gemini creative prompt via your API for cross-channel content."""
    if not GEMINI_API_KEY:
        return "[ERROR] GEMINI_API_KEY environment variable not set."

    payload = {
        "contents": [{
            "parts": [
                {"text": f"Write a powerful multilingual post announcing this eBook: {title}. Message: {content}"}
            ]
        }]
    }
    headers = {
        # "Authorization": f"Bearer {GEMINI_API_KEY}",  # This line is commented out as the API key is not valid
        "Content-Type": "application/json"
    }
    # The following lines are commented out to prevent actual API calls during testing
    # response = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
    #                          headers=headers, json=payload)
    # try:
    #     return response.json()['candidates'][0]['content']['parts'][0]['text']
    # except:
    #     return "[ERROR] Gemini response invalid."
    return f"[INFO] Gemini blast for '{title}' was not sent because the integration is not fully implemented."


# === MASTER EBOOK LAUNCH ===

from . import storage
from . import x_client

def launch_wave(titles: List[str]):
    """
    Launches a promotional wave for a list of book titles.
    """
    print(f"Starting launch wave for {len(titles)} titles...")
    for title in titles:
        url = f"{BOOKS_CATALOG_URL}&q={'+'.join(title.split())}"
        ping_indexing_signal(title, url)
        post = post_gemini_blast(title, SHORT_DESC)

        print("\n==== GENERATED POST ====")
        print(post)
        print("========================\n")
    print(f"Launch wave completed for {len(titles)} titles.")

def launch_campaign(campaign_id: str):
    """
    Launches a promotional campaign by posting to X.
    """
    print(f"Launching campaign {campaign_id}...")
    campaign = storage.load_campaign_by_id(campaign_id)
    if not campaign:
        print(f"[ERROR] Campaign {campaign_id} not found.")
        return

    # Get X API credentials from environment variables
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    for book_id in campaign.get("book_ids", []):
        book = storage.load_book_by_id(book_id)
        if not book:
            print(f"[WARNING] Book with ID {book_id} not found in storage.")
            continue

        book_title = book.get("volumeInfo", {}).get("title", "Unknown Title")
        # In a real app, you would get this from your own domain
        book_url = f"http://localhost:8000/books/{book_id}"

        # Construct the tweet
        message = f"{campaign['promo_message']}\n\nCheck out '{book_title}'!\n{book_url}"

        x_client.post_tweet(message, api_key, api_secret, access_token, access_token_secret)

    print(f"Campaign {campaign_id} launched successfully.")

import os
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from . import launch
from . import google_books_client
from . import storage

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class LaunchRequest(BaseModel):
    titles: List[str]

class IngestRequest(BaseModel):
    author_name: str

class CampaignCreate(BaseModel):
    name: str
    book_ids: List[str]
    promo_message: str

@app.get("/")
def read_root():
    return {"message": "Growth OS API is running."}

@app.post("/launch")
async def launch_endpoint(request: LaunchRequest, background_tasks: BackgroundTasks):
    """
    Accepts a list of book titles and triggers the launch wave in the background.
    """
    background_tasks.add_task(launch.launch_wave, request.titles)
    return {"message": "Launch wave initiated in the background."}

@app.post("/ingest/google-books")
async def ingest_google_books_endpoint(request: IngestRequest):
    """
    Ingests books by a given author from the Google Books API and saves them to storage.
    """
    google_books_api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    if not google_books_api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_BOOKS_API_KEY environment variable not set.")

    books = google_books_client.fetch_books_by_author(request.author_name, google_books_api_key)
    if not books:
        return {"message": f"No books found for author '{request.author_name}'."}

    storage.save_books(books)
    return {"message": f"Successfully ingested {len(books)} books by '{request.author_name}'."}

@app.get("/books/{book_id}", response_class=HTMLResponse)
async def get_book_page(request: Request, book_id: str):
    """
    Renders an HTML page for a specific book.
    """
    book = storage.load_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return templates.TemplateResponse(request=request, name="book.html", context={"book": book})

@app.post("/campaigns", status_code=201)
async def create_campaign(campaign: CampaignCreate):
    """
    Creates a new promotional campaign.
    """
    campaign_dict = campaign.model_dump()
    new_campaign = storage.save_campaign(campaign_dict)
    if not new_campaign:
        raise HTTPException(status_code=500, detail="Failed to create campaign.")
    return new_campaign

@app.post("/campaigns/{campaign_id}/launch")
async def launch_campaign_endpoint(campaign_id: str, background_tasks: BackgroundTasks):
    """
    Launches a promotional campaign in the background.
    """
    background_tasks.add_task(launch.launch_campaign, campaign_id)
    return {"message": f"Campaign {campaign_id} launch initiated in the background."}

@app.get("/track/{book_id}")
async def track_click(book_id: str):
    """
    Logs a click event for a book and redirects to the book's page.
    """
    event_data = {
        "event_type": "click",
        "book_id": book_id,
    }
    storage.log_event(event_data)

    return RedirectResponse(url=f"/books/{book_id}", status_code=307)

@app.get("/analytics")
async def get_analytics():
    """
    Returns a summary of the analytics data.
    """
    metrics = storage.load_metrics()

    total_clicks = 0
    clicks_per_book = {}

    for event in metrics:
        if event.get("event_type") == "click":
            total_clicks += 1
            book_id = event.get("book_id")
            if book_id:
                clicks_per_book[book_id] = clicks_per_book.get(book_id, 0) + 1

    return {
        "total_clicks": total_clicks,
        "clicks_per_book": clicks_per_book,
    }

import os
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.responses import HTMLResponse
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

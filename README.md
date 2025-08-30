# Growth OS API

API to trigger a promotional launch wave for eBooks.

## Setup
- `pip install -r requirements.txt`
- Set `GEMINI_API_KEY` environment variable.

## Run
`uvicorn app.main:app --reload`

## Usage
`POST /launch` with `{"titles": ["Book 1", "Book 2"]}`

## Testing
`python -m pytest`
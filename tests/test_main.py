from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Growth OS API is running."}

def test_launch_endpoint():
    response = client.post("/launch", json={"titles": ["Book 1", "Book 2"]})
    assert response.status_code == 200
    assert response.json() == {"message": "Launch wave initiated in the background."}

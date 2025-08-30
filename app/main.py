from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List
from . import launch

app = FastAPI()

class LaunchRequest(BaseModel):
    titles: List[str]

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

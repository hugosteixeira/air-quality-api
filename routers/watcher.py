from fastapi import APIRouter, BackgroundTasks
from App.DataWatcher import DataWatcher

router = APIRouter()
data_watcher = DataWatcher()

@router.get("/start_watcher")
def start_watcher():
    data_watcher = DataWatcher()
    data_watcher.run()
    return {"message": "Data watcher started"}

@router.post("/stop_watcher")
def stop_watcher():
    # Implement a way to stop the watcher if needed
    return {"message": "Data watcher stopped"}

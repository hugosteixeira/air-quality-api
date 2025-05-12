from fastapi import APIRouter, BackgroundTasks
from DataWatcher import DataWatcher

router = APIRouter()
data_watcher = DataWatcher()

@router.get("/start_watcher")
def start_watcher():
    data_watcher = DataWatcher()
    data_watcher.start()
    return {"message": "Data watcher started"}

@router.get("/run")
def start_watcher():
    data_watcher = DataWatcher()
    data_watcher.run()
    return {"message": "Data watcher runned"}

@router.post("/stop_watcher")
def stop_watcher():
    return {"message": "Data watcher stopped"}

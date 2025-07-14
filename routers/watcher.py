from fastapi import APIRouter, BackgroundTasks
from DataWatcher import DataWatcher
import threading

router = APIRouter()
data_watcher = DataWatcher()
watcher_thread = None  # Track the watcher thread

@router.get("/start_watcher")
def start_watcher():
    global watcher_thread
    if watcher_thread and watcher_thread.is_alive():
        return {"message": "Data watcher is already running"}
    watcher_thread = data_watcher.start()
    return {"message": "Data watcher started"}

@router.get("/run")
def start_watcher():
    data_watcher = DataWatcher()
    data_watcher.run()
    return {"message": "Data watcher runned"}

@router.post("/stop_watcher")
def stop_watcher():
    global watcher_thread
    data_watcher.stop()
    if watcher_thread and watcher_thread.is_alive():
        watcher_thread.join(timeout=2)
        watcher_thread = None
    return {"message": "Data watcher stopped"}

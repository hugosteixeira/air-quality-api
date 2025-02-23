import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import data, watcher
import threading
from DataWatcher import DataWatcher

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(data.router)
app.include_router(watcher.router)

def start_data_watcher():
    data_watcher = DataWatcher()
    data_watcher.start()

if __name__ == "__main__":
    watcher_thread = threading.Thread(target=start_data_watcher)
    watcher_thread.start()
    uvicorn.run(app, host="0.0.0.0")
from fastapi import FastAPI
from App.routers import data, watcher

app = FastAPI()

app.include_router(data.router)
app.include_router(watcher.router)

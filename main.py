import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from App.routers import data, watcher

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

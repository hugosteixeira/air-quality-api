import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import data, watcher
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import ssl

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(data.router)
app.include_router(watcher.router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
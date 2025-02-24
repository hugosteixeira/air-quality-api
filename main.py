import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import data, watcher
import threading
from DataWatcher import DataWatcher
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import ssl


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
app.add_middleware(HTTPSRedirectMiddleware)


app.include_router(data.router)
app.include_router(watcher.router)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('/etc/ssl/certs/apache-selfsigned.crt', keyfile='/etc/ssl/private/apache-selfsigned.key')

def start_data_watcher():
    data_watcher = DataWatcher()
    data_watcher.start()

if __name__ == "__main__":
    watcher_thread = threading.Thread(target=start_data_watcher)
    watcher_thread.start()
    uvicorn.run(app, ssl=ssl_context)
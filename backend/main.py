import logging

from fastapi import FastAPI
from backend.api.routes.scan import router as scan_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s"
)

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(scan_router)
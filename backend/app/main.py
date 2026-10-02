from pathlib import Path
from dotenv import load_dotenv

# Load .env before any app modules are imported so that singleton services
# (e.g. vqa_service, grounding_service) read the correct env vars at init time.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router
from app.api.preview import router as preview_router
from app.api.pixel import router as pixel_router
from app.api.catalog import router as catalog_router
from app.api.analysis import router as analysis_router
from app.api.vqa import router as vqa_router
from app.api.grounding import router as grounding_router
from app.api.export import router as export_router


app = FastAPI(
    title="SatQuery AI",
    description="Agentic Vision-Language Assistant for Remote Sensing",
    version="0.1.0"
)

# Enable CORS for frontend API calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(preview_router)
app.include_router(pixel_router)
app.include_router(catalog_router)
app.include_router(analysis_router)
app.include_router(vqa_router)
app.include_router(grounding_router)
app.include_router(export_router)


@app.get("/")
def root():
    return {
        "project": "SatQuery AI",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

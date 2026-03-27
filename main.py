import os
import sys

from dotenv import load_dotenv

load_dotenv()

_REQUIRED_ENV_VARS = [
    "CLOUDINARY_CLOUD_NAME",
    "CLOUDINARY_API_KEY",
    "CLOUDINARY_API_SECRET",
    "KIE_API_KEY",
]

_missing = [v for v in _REQUIRED_ENV_VARS if not os.getenv(v)]
if _missing:
    print(
        "\n[ERROR] The following required environment variables are not set:\n"
        + "\n".join(f"  - {v}" for v in _missing)
        + "\n\nCopy .env.example to .env and fill in your credentials, then restart.\n",
        file=sys.stderr,
    )
    sys.exit(1)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routes.upload import router as upload_router
from routes.process import router as process_router

app = FastAPI(title="Tile Place Flux01")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(process_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

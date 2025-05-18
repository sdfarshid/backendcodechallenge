from pathlib import Path

from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.api.v1.routers import api_router
from app.utilities.log import logger, DebugWaring





app = FastAPI(
    title="Fetcher Service",
    version="1.0",
    description="Fetch commits",
    debug=True
)

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    logger.info("Service started")


@app.get("/")
async def home(request: Request):
    data = {
        "title": "welcome",
        "header": "welcome",
    }
    return templates.TemplateResponse("index.html", {"request": request, **data})

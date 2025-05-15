from fastapi import FastAPI

from app.api.v1.routers import api_router
from app.utilities.log import logger, DebugWaring

app = FastAPI(
    title="Fetcher Service",
    version="1.0",
    description="Fetch commits",
    debug=True
)


app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup():
    logger.info("Service started")



@app.get("/")
async def root():
    DebugWaring("Root endpoint accessed")
    return {"message": "Hello Fetcher Service!"}


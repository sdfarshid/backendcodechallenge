from fastapi import FastAPI

from app.utilities.log import logger, DebugWaring

app = FastAPI(
    title="Fetcher Service",
    version="1.0",
    description="Fetch commits",
    debug=True
)



@app.get("/")
async def root():
    DebugWaring("Root endpoint accessed")
    return {"message": "Hello Fetcher Service!"}


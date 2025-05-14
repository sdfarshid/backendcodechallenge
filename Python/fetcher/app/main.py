from fastapi import FastAPI


app = FastAPI(
    title="Fetcher Service",
    version="1.0",
    description="Fetch commits",
    debug=True
)



@app.get("/")
async def root():
    return {"message": "Hello Fetcher Service!"}


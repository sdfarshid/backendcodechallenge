from fastapi import APIRouter

from app.api.v1.endpoint import fetch, commit, author

api_router  =APIRouter()


api_router.include_router(fetch.router, prefix="/fetching", tags=["fetch"])

api_router.include_router(commit.router, prefix="/commit", tags=["commit"])

api_router.include_router(author.router, prefix="/author", tags=["author"])
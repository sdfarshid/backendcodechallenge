from fastapi import APIRouter

from app.api.v1.endpoint import fetch

api_router  =APIRouter()


api_router.include_router(fetch.router, prefix="/fetch", tags=["fetch"])
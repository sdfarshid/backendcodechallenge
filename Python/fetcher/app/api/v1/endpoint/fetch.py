from fastapi import APIRouter

from app.application.commands.fetch_commits import FetchCommitsCommand

router = APIRouter()


@router.post("/fetch")
async def fetching_commits(command: FetchCommitsCommand):
    pass
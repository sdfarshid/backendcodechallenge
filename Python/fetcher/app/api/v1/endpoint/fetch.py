from fastapi import APIRouter, Depends, BackgroundTasks

from app.application.commands.fetch_commits import FetchCommitsCommand
from app.application.services.fetcher_service import FetcherService
from app.config.dependencies.services import get_fetcher_service
from app.utilities.helper import handle_exceptions

router = APIRouter()





@router.post("/fetch")
@handle_exceptions
async def fetching_commits(
    command: FetchCommitsCommand,
    service: FetcherService = Depends(get_fetcher_service)
):
     return await service.fetch_and_store_commits(command=command)


@router.post("/back-fetching")
@handle_exceptions
async def back_fetching_commits(
    command: FetchCommitsCommand,
    background_tasks: BackgroundTasks,
    service: FetcherService = Depends(get_fetcher_service)
):
    background_tasks.add_task(service.fetch_and_store_commits, command)
    return {"message": f"Fetch started in background (count: {command.count})"}


from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.commands.fetch_commits import FetchCommitsCommand
from app.application.services.fetcher_service import FetcherService
from app.utilities.helper import handle_exceptions

router = APIRouter()

ServiceDependency = Annotated[FetcherService, Depends(FetcherService)]



@router.post("/fetch")
@handle_exceptions
async def fetching_commits(command: FetchCommitsCommand, service: ServiceDependency):
     return await service.fetch_and_store_commits(command=command)

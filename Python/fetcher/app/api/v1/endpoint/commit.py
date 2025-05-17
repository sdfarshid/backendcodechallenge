from typing import Optional, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.application.mixins.pagination import PaginationParams, get_pagination_params
from app.application.queries.list_commits import ListCommitsQuery
from app.application.services.commit_service import CommitService
from app.config.dependencies.services import get_commit_service
from app.utilities.helper import handle_exceptions

router = APIRouter()


ServiceDependency = Annotated[CommitService, Depends(get_commit_service)]



@router.get("/list")
@handle_exceptions
async def get_commits(
            service: ServiceDependency,
            pagination: PaginationParams = Depends(get_pagination_params),
            author_id: Optional[UUID] = Query(None, description="ID of the author to filter commits")
            ):

    query = ListCommitsQuery(pagination=pagination, author_id=author_id)
    return await  service.get_commit(query)


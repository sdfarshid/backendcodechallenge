from typing import  Annotated

from fastapi import APIRouter, Depends, Query

from app.application.mixins.pagination import PaginationParams, get_pagination_params
from app.application.queries.list_authors import ListAuthorsQuery
from app.application.services.author_service import AuthorService
from app.config.dependencies.services import get_author_service
from app.utilities.helper import handle_exceptions

router = APIRouter()


ServiceDependency = Annotated[AuthorService, Depends(get_author_service)]



@router.get("/list")
@handle_exceptions
async def get_commits(
            service: ServiceDependency,
            pagination: PaginationParams = Depends(get_pagination_params)
            ):

    query = ListAuthorsQuery(pagination=pagination)
    return await  service.list_authors(query)


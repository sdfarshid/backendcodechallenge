
from pydantic import BaseModel
from app.application.mixins.pagination import PaginationParams


class ListAuthorsQuery(BaseModel):
    pagination: PaginationParams
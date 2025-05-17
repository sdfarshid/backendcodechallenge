import uuid
from typing import Optional

from pydantic import BaseModel

from app.application.mixins.pagination import PaginationParams


class ListCommitsQuery(BaseModel):
    pagination: PaginationParams
    author_id: Optional[uuid.UUID] = None

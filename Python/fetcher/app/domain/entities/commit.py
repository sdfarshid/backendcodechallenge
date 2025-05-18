import datetime
from typing import Optional
from uuid import uuid4, UUID
from pydantic import BaseModel, Field


class Commit(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    hash: str
    author_id: UUID
    created_at: Optional[datetime.datetime] = None

from uuid import uuid4, UUID
from pydantic import BaseModel


class Commit(BaseModel):
    id: UUID = uuid4()
    hash: str
    author_id: UUID


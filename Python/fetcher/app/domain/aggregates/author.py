from uuid import UUID, uuid4
from pydantic import BaseModel


class Author(BaseModel):
    id: UUID = uuid4()
    name:str
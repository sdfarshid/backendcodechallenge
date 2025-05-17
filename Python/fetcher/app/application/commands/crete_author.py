from typing import List
from uuid import UUID

from pydantic import BaseModel
from typing_extensions import Dict


class CreateAuthorCommand(BaseModel):
    unique_author_names: List[str]
    existing_author_map: Dict[str, UUID]


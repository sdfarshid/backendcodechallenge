from typing import List
from uuid import UUID

from pydantic import BaseModel
from typing_extensions import Dict


class StoreCommitsCommand(BaseModel):
    grouped_commits: Dict[UUID, List[dict]]
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.application.mixins.pagination import PaginationParams
from app.domain.entities.commit import Commit


class ICommitRepository (ABC):

    @abstractmethod
    async def add_commits_batch(self, commits: List[Commit]) -> int:
        pass

    @abstractmethod
    async def list_commits(self, pagination: PaginationParams, author_id: Optional[UUID]) -> List[Commit] | None:
        pass

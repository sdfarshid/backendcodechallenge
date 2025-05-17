from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.application.mixins.pagination import PaginationParams
from app.domain.entities.commit import Commit


class ICommitRepository (ABC):

    @abstractmethod
    async def add_commits_batch(self, commits: List[Commit]) -> int:
        pass

    @abstractmethod
    async def get_commit_by_author_id(self, author_id: UUID, pagination: PaginationParams) -> List[Commit] | None:
        pass

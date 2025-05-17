from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from app.application.mixins.pagination import PaginationParams
from app.domain.aggregates.author import Author


class IAuthorRepository(ABC):

    @abstractmethod
    async def get_author_by_name(self, name: str) -> Author | None:
        pass

    @abstractmethod
    async def get_authors_by_names(self, name: list[str]) -> List[Author] | None:
        pass

    @abstractmethod
    async def add_author(self, author: Author) -> Author:
        pass

    async def list_authors(self, pagination: PaginationParams) -> List[Author] | None:
        pass


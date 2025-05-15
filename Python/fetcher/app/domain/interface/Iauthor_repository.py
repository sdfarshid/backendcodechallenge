from __future__ import annotations
from abc import ABC, abstractmethod
from app.domain.aggregates.author import Author


class IAuthorRepository(ABC):

    @abstractmethod
    async def get_author_by_name(self, name: str) -> Author | None:
        pass

    @abstractmethod
    async def add_author(self, author: Author) -> Author:
        pass


from __future__ import annotations

from typing import List

from app.application.queries.list_authors import ListAuthorsQuery
from app.domain.aggregates.author import Author
from app.domain.interface.Iauthor_repository import IAuthorRepository


class ListAuthorsHandler:
    def __init__(self, repository: IAuthorRepository, logger):
        self.repository = repository
        self.logger = logger

    async def handle(self, query: ListAuthorsQuery) -> List[Author] | None:
        return await self.repository.list_authors(query.pagination)

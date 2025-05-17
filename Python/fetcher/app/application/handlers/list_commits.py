from __future__ import annotations

from typing import List

from app.application.queries.list_commits import ListCommitsQuery
from app.domain.entities.commit import Commit
from app.domain.interface.Icommit_repository import ICommitRepository


class ListCompaniesHandler:
    def __init__(self, commit_repository: ICommitRepository, logger):
        self.commit_repository = commit_repository
        self.logger = logger

    async def handle(self, query: ListCommitsQuery) -> List[Commit] | None:
        return await self.commit_repository.list_commits(query.pagination,query.author_id)

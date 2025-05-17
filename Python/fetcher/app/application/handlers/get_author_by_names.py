from fastapi import Depends

from app.application.queries.get_authors_by_name import GetAuthorsByNamesQuery
from app.domain.interface.Iauthor_repository import IAuthorRepository
from app.infrastructure.repositories.author_repository import AuthorRepository
from app.utilities.log import commit_logger


class GetAuthorsByNamesCommandHandler:

    def __init__(self, author_repository: IAuthorRepository, logger):
        self.repository = author_repository
        self.logger = commit_logger


    async def handle(self, query: GetAuthorsByNamesQuery) -> dict:
        try:
            existing_authors = await self.repository.get_authors_by_names(query.unique_author_names)
            return {author.name: author.id for author in existing_authors}
        except Exception as e:
            self.logger.error(f"Failed to store  GetAuthorByNamesCommandHandler : {e}")
            raise RuntimeError(f"Failed fetching users : {e}")



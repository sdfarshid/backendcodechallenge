from typing import Dict

from fastapi import Depends

from app.application.commands.crete_author import CreateAuthorCommand
from app.domain.aggregates.author import Author
from app.domain.interface.Iauthor_repository import IAuthorRepository
from app.infrastructure.repositories.author_repository import AuthorRepository
from app.utilities.log import commit_logger


class CreateAuthorCommandHandler:

    def __init__(self, author_repository: IAuthorRepository, logger):
        self.repository = author_repository
        self.logger = logger


    async def handle(self, command: CreateAuthorCommand) -> Dict:
        try:
            new_authors = []
            existing_author_map = command.existing_author_map

            for name in  set(command.unique_author_names):
                if name not in existing_author_map:
                    new_author = Author(name=name)
                    new_authors.append(new_author)

            for author in new_authors:
                await self.repository.add_author(author)
                existing_author_map[author.name] = author.id

            return existing_author_map

        except Exception as e:
            self.logger.error(f"Failed to store authors in CreateAuthorCommandHandler: {e}")
            raise RuntimeError(f"Failed storing authors: {e}")

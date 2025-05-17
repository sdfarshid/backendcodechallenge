from fastapi import Depends

from app.config.dependencies.repositories import get_author_repository, get_commit_repository
from app.domain.interface.Iauthor_repository import IAuthorRepository
from app.domain.interface.Icommit_repository import ICommitRepository
from app.infrastructure.repositories.author_repository import AuthorRepository
from app.infrastructure.repositories.commit_repository import CommitRepository
from app.application.handlers.create_author import CreateAuthorCommandHandler
from app.application.handlers.get_author_by_names import GetAuthorsByNamesCommandHandler
from app.application.handlers.store_commits import StoreCommitsCommandHandler
from app.utilities.log import commit_logger


def get_create_author_handler(repo: IAuthorRepository = Depends(get_author_repository)) -> CreateAuthorCommandHandler:
    return CreateAuthorCommandHandler(repo, commit_logger)



def get_get_authors_by_name_handler(repo: IAuthorRepository = Depends(get_author_repository)) -> GetAuthorsByNamesCommandHandler:
    return GetAuthorsByNamesCommandHandler(repo, commit_logger)


def get_store_commits_handler(repo: ICommitRepository = Depends(get_commit_repository)) -> StoreCommitsCommandHandler:
    return StoreCommitsCommandHandler(repo, commit_logger)

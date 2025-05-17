from fastapi import Depends

from app.application.handlers.create_author import CreateAuthorCommandHandler
from app.application.handlers.get_author_by_names import GetAuthorsByNamesCommandHandler
from app.application.handlers.store_commits import StoreCommitsCommandHandler
from app.application.services.commit_service import CommitService
from app.application.services.fetcher_service import FetcherService
from app.application.services.author_service import AuthorService
from app.infrastructure.fetchers.fetcher_factory import FetcherFactory
from app.utilities.log import commit_logger, fetcher_logger
from app.config.dependencies.handlers import (
    get_store_commits_handler,
    get_create_author_handler,
    get_get_authors_by_name_handler,
)

def get_commit_service(
    store_handler: StoreCommitsCommandHandler = Depends(get_store_commits_handler)
) -> CommitService:
    return CommitService(store_handler, commit_logger)

def get_author_service(
    create_handler: CreateAuthorCommandHandler = Depends(get_create_author_handler),
    filter_handler: GetAuthorsByNamesCommandHandler = Depends(get_authors_by_name_handler),
    get_list_handler: GetAuthorsByNamesCommandHandler = Depends(get_list_authors_handler)
) -> AuthorService:
    return AuthorService(get_author_by_name_handler=filter_handler,
                         get_list_authors_handler = get_list_handler,
                         create_author_handler=create_handler)

def get_fetcher_service(
    author_service: AuthorService = Depends(get_author_service),
    commit_service: CommitService = Depends(get_commit_service)
) -> FetcherService:
    fetcher_factory = FetcherFactory()
    return FetcherService(fetcher_factory, author_service, commit_service, fetcher_logger)
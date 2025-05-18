import asyncio
import argparse


from app.application.commands.fetch_commits import FetchCommitsCommand
from app.application.handlers.list_authors import ListAuthorsHandler
from app.application.services.fetcher_service import FetcherService
from app.application.services.author_service import AuthorService
from app.application.services.commit_service import CommitService
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.fetchers.fetcher_factory import FetcherFactory
from app.infrastructure.repositories.author_repository import AuthorRepository
from app.infrastructure.repositories.commit_repository import CommitRepository
from app.application.handlers.store_commits import StoreCommitsCommandHandler
from app.application.handlers.create_author import CreateAuthorCommandHandler
from app.application.handlers.get_author_by_names import GetAuthorsByNamesCommandHandler
from app.application.handlers.list_commits import ListCompaniesHandler
from app.utilities.log import fetcher_logger, commit_logger


async def get_fetcher_service() -> FetcherService:
    async with AsyncSessionLocal() as db:
        author_repo = AuthorRepository(db)
        commit_repo = CommitRepository(db)

        store_commits_handler = StoreCommitsCommandHandler(commit_repo,commit_logger)
        list_commits_handler = ListCompaniesHandler(commit_repo,commit_logger)

        create_author_handler = CreateAuthorCommandHandler(author_repo,commit_logger)
        get_authors_by_name_handler = GetAuthorsByNamesCommandHandler(author_repo,commit_logger)
        list_authors_handler = ListAuthorsHandler(author_repo,commit_logger)

        author_service = AuthorService(
            get_author_by_name_handler=get_authors_by_name_handler,
            get_list_authors_handler=list_authors_handler,
            create_author_handler=create_author_handler,
        )

        commit_service = CommitService(
            store_commits_handler=store_commits_handler,
            list_commits_handler=list_commits_handler,
            logger=commit_logger,
        )

        fetcher_service = FetcherService(
            fetcher_factory=FetcherFactory(),
            author_service=author_service,
            commit_service=commit_service,
            logger=fetcher_logger
        )

        return fetcher_service


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10, help="Number of commits to fetch")
    args = parser.parse_args()

    service = await get_fetcher_service()
    command = FetchCommitsCommand(count=args.count)
    result = await service.fetch_and_store_commits(command)

    print("Done. Stored commits:", result.get("stored_commits", 0))


if __name__ == "__main__":
    asyncio.run(main())

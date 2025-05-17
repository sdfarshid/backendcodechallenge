import asyncio
from collections import defaultdict
from typing import List, Dict

from fastapi import Depends

from app.application.commands.crete_author import CreateAuthorCommand
from app.application.commands.fetch_commits import FetchCommitsCommand
from app.application.commands.store_commits import StoreCommitsCommand
from app.application.handlers.create_author import CreateAuthorCommandHandler
from app.application.handlers.get_author_by_names import GetAuthorsByNamesCommandHandler
from app.application.handlers.store_commits import StoreCommitsCommandHandler
from app.application.queries.get_authors_by_name import GetAuthorsByNamesQuery
from app.domain.aggregates.author import Author
from app.domain.enums.fetchet_source import FetcherSource
from app.infrastructure.fetchers.fetcher_factory import FetcherFactory
from tenacity import retry, stop_after_attempt, wait_exponential
from app.utilities.log import DebugWaring, commit_logger


class FetcherService:

    def __init__(self,
                 get_author_by_name_handler: GetAuthorsByNamesCommandHandler = Depends(GetAuthorsByNamesCommandHandler),
                 create_author_handler: CreateAuthorCommandHandler = Depends(CreateAuthorCommandHandler),
                 store_commits_handler: StoreCommitsCommandHandler = Depends(StoreCommitsCommandHandler),
                 fetcher_factory: FetcherFactory = Depends(FetcherFactory),
                 ):
        self.get_author_by_name_handler = get_author_by_name_handler
        self.create_author_handler = create_author_handler
        self.fetcher_factory = fetcher_factory
        self.store_commits_handler = store_commits_handler
        self.semaphore = asyncio.Semaphore(5)
        self.logger = commit_logger


    async def fetch_and_store_commits(self, command: FetchCommitsCommand):
        try:

            commit_lists = await  self._parallel_fetching(command)
            flat_commits = await  self.__collect_and_flating_commits(commit_lists)
            all_commits = flat_commits[:command.count]

            all_existing_author_map = await self._manage_authors(all_commits)
            grouped_commits = await self.__collecting_authors_commits(all_commits, all_existing_author_map)

            stored_commits =  await self._store_authors_commits(grouped_commits)

            return {"message": "commits fetching successfully", "stored_commits": stored_commits}

        except Exception as e:
            self.logger.error(f"Have failed fetching commits: {e}")
            raise


    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _parallel_fetching(self, command: FetchCommitsCommand) -> List[List[Dict]]:
        fetcher = self.fetcher_factory.create_fetcher(FetcherSource.GITHUB)
        default_per_page = fetcher.default_per_page
        total_pages = (command.count + default_per_page - 1) // default_per_page

        async def fetch_page(page):
            async with self.semaphore:
                try:
                    result = await fetcher.fetch(default_per_page, page)
                    if not result:
                        self.logger.warning(f"No results in page {page}")
                    return result
                except Exception as e:
                    self.logger.error(f"Failed to fetch page {page}: {str(e)}")
                    return []

        tasks = [fetch_page(p) for p in range(1, total_pages + 1)]
        return await asyncio.gather(*tasks, return_exceptions=False)


    async def __collect_and_flating_commits(self, commit_lists) -> list:
        """
          Collect and Flat all commits from the GitHub repository.
            [
                [commit1, commit2],
                [commit3, commit4],
                [commit5]
            ]
        """
        flat_commits = []
        for commit_list in commit_lists:
            flat_commits.extend(commit_list)

        return  flat_commits


    async def _manage_authors(self, all_commits:list) -> Dict :

        unique_author_names = list(set(commit["author"].strip() for commit in all_commits))

        query = GetAuthorsByNamesQuery(unique_author_names=unique_author_names)
        existing_author_map = await self.get_author_by_name_handler.handle(query)

        return  await self._store_new_authors(unique_author_names, existing_author_map)


    async def _store_new_authors(self, unique_author_names: list[str], existing_author_map: dict ) -> Dict:

        command = CreateAuthorCommand(
            unique_author_names = unique_author_names,
            existing_author_map = existing_author_map
        )
        return  await self.create_author_handler.handle(command)


    async def __collecting_authors_commits(self, all_commits: list, all_existing_author_map: dict) -> Dict :

        grouped_commits = defaultdict(list)
        for commit in all_commits:
            author_name = commit["author"].strip()
            author_id = all_existing_author_map.get(author_name)
            if not author_id:
                continue
            grouped_commits[author_id].append(commit)

        return  grouped_commits

    async def _store_authors_commits(self, grouped_commits) -> int:
        store_command = StoreCommitsCommand(grouped_commits=grouped_commits)
        return  await self.store_commits_handler.handle(store_command)


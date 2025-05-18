import asyncio
from collections import defaultdict
from typing import List, Dict


from app.application.commands.fetch_commits import FetchCommitsCommand
from app.domain.enums.fetchet_source import FetcherSource
from tenacity import retry, stop_after_attempt, wait_exponential


class FetcherService:

    def __init__(self, fetcher_factory, author_service, commit_service, logger):
        self.fetcher_factory = fetcher_factory
        self.author_service = author_service
        self.commit_service = commit_service
        self.semaphore = asyncio.Semaphore(5)
        self.logger = logger

    async def fetch_and_store_commits(self, command: FetchCommitsCommand):
        try:

            commit_lists = await  self._parallel_fetching(command)
            flat_commits = await  self.__collect_and_flating_commits(commit_lists)
            all_commits = flat_commits[:command.count]

            all_existing_author_map = await self.author_service.manage_authors(all_commits)

            stored_commits =  await self.commit_service.process_and_store_commits(all_commits, all_existing_author_map)

            self.logger.info(f"commits fetching successfully stored_commits: {stored_commits}")

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
                    self.logger.info(f"Fetching page {page}")

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
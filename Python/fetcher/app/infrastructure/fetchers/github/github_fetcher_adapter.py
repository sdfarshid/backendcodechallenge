from typing import Dict, List
from fastapi import Depends

from app.config.dependencies import get_github_token, get_github_repo
from app.infrastructure.fetchers.fetcher_adapter_interface import FetcherAdapterInterface
from app.infrastructure.fetchers.github.github_fetcher import GithubFetcher


class GithubFetcherAdapter(FetcherAdapterInterface):
    DEFAULT_PER_PAGE = 100

    def __init__(
        self,
        token: str = Depends(get_github_token),
        repo: str = Depends(get_github_repo),
    ):
        self.repo = repo
        self.github_fetcher = GithubFetcher(token=token,per_page=self.DEFAULT_PER_PAGE)


    async def fetch(self, count: int) -> List[Dict]:
        commits = []
        pages = (count + self.DEFAULT_PER_PAGE - 1)

        for page in range(1, pages + 1):
            if len(commits) >= count:
                break

            raw_commits = await self.github_fetcher.fetch_raw_commits(self.repo, page)

            for commit in raw_commits:
                adapted_commit = {
                    "hash": commit["sha"],
                    "author": commit["author"]["login"] if commit.get("author") else "unknown"
                }
                commits.append(adapted_commit)

            if len(raw_commits) < self.DEFAULT_PER_PAGE:
                break

        return commits[:count]

from typing import Dict, List, Optional
from app.infrastructure.fetchers.fetcher_adapter_interface import FetcherAdapterInterface
from app.infrastructure.fetchers.github.github_fetcher import GithubFetcher


class GithubFetcherAdapter(FetcherAdapterInterface):
    _DEFAULT_PER_PAGE = 100

    def __init__(self, token: str, repo: str):
        self.repo = repo
        self.github_fetcher = GithubFetcher(token=token, per_page=self._DEFAULT_PER_PAGE)


    @property
    def default_per_page(self) -> int:
        return self._DEFAULT_PER_PAGE


    async def fetch(self, page: int) -> List[Dict]:
        raw_commits = await self.github_fetcher.fetch_raw_commits(self.repo, page)
        commits = []
        for commit in raw_commits:
            commits.append({
                "hash": commit["sha"],
                "author": commit["author"]["login"] if commit.get("author") else "unknown",
                "created_at": commit["commit"]["author"]["date"]
            })
        return commits

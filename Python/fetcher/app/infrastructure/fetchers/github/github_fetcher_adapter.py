from typing import Dict, List
from app.infrastructure.fetchers.fetcher_adapter_interface import FetcherAdapterInterface
from app.infrastructure.fetchers.github.github_fetcher import GithubFetcher


class GithubFetcherAdapter(FetcherAdapterInterface):

    def __init__(self, github_fetcher: GithubFetcher, repo: str):
        self.github_fetcher = github_fetcher
        self.repo = repo


    @property
    def default_per_page(self) -> int:
        return self.github_fetcher.DEFAULT_PER_PAGE


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

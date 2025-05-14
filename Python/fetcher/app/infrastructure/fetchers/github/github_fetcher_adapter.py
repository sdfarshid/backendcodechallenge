from typing import Dict, List
from fastapi import Depends

from app.config.dependencies import get_github_token, get_github_repo
from app.infrastructure.fetchers.fetcher_adapter_interface import FetcherAdapterInterface
from app.infrastructure.fetchers.github.github_fetcher import GithubFetcher


class GithubFetcherAdapter(FetcherAdapterInterface):
    def __init__(
        self,
        github_fetcher: GithubFetcher = Depends(GithubFetcher),
        token: str = Depends(get_github_token),
        repo: str = Depends(get_github_repo),
    ):
        self.github_fetcher = github_fetcher
        self.token = token
        self.repo = repo

    async def fetch(self, count: int) -> List[Dict]:
        commits = []
        per_page = 100
        pages = (count + per_page - 1)

        for page in range(1, pages + 1):
            if len(commits) >= count:
                break

            raw_commits = await self.github_fetcher.fetch_raw_commits(
                self.token, self.repo, per_page, page
            )
            for commit in raw_commits:
                adapted_commit = {
                    "hash": commit["sha"],
                    "author": commit["author"]["login"] if commit.get("author") else "unknown"
                }
                commits.append(adapted_commit)

            if len(raw_commits) < per_page:
                break

        return commits[:count]

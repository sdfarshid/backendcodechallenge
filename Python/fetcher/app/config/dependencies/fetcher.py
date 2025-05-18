from app.config.dependencies.settings import get_github_token
from app.infrastructure.fetchers.github.github_fetcher import GithubFetcher


def get_github_fetcher() -> GithubFetcher:
    return GithubFetcher(
        token=get_github_token(),
        per_page=100
    )
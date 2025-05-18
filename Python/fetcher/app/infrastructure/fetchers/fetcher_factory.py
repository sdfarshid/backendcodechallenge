from app.config.dependencies.fetcher import get_github_fetcher
from app.config.dependencies.settings import get_github_token, get_github_repo
from app.domain.enums.fetchet_source import FetcherSource
from app.infrastructure.fetchers.fetcher_adapter_interface import FetcherAdapterInterface
from app.infrastructure.fetchers.github.github_fetcher_adapter import GithubFetcherAdapter


class FetcherFactory:
    FETCHERS = {
        FetcherSource.GITHUB: lambda: GithubFetcherAdapter(
            github_fetcher=get_github_fetcher(),
            repo=get_github_repo()
        )
    }


    @staticmethod
    def create_fetcher(source: str) -> FetcherAdapterInterface:
        source = source.lower()
        if source in FetcherFactory.FETCHERS:
            return FetcherFactory.FETCHERS[source]()
        else:
            raise ValueError(f"Unsupported source : {source}")

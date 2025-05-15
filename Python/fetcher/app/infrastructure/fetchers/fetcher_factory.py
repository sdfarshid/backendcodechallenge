from app.domain.enums.fetchet_source import FetcherSource
from app.infrastructure.fetchers.fetcher_adapter_interface import FetcherAdapterInterface
from app.infrastructure.fetchers.github.github_fetcher_adapter import GithubFetcherAdapter


class FetcherFactory:
    FETCHERS = {
        FetcherSource.GITHUB: GithubFetcherAdapter
    }


    @staticmethod
    def create_fetcher(source: str) -> FetcherAdapterInterface:
        source = source.lower()
        if source in FetcherFactory.FETCHERS:
            return FetcherFactory.FETCHERS[source]()
        else:
            raise ValueError(f"Unsupported source : {source}")

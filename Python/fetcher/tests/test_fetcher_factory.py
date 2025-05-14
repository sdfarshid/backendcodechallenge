
from app.infrastructure.fetchers.fetcher_factory import FetcherFactory
from app.infrastructure.fetchers.github.github_fetcher_adapter import GithubFetcherAdapter


def test_create_fetcher_github():
    fetcher = FetcherFactory.create_fetcher("github")
    assert isinstance(fetcher, GithubFetcherAdapter)


def test_create_fetcher_unsupported():
    try:
        FetcherFactory.create_fetcher("unknown")
        assert False
    except ValueError:
        pass
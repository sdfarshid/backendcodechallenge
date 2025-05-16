import pytest
from app.infrastructure.fetchers.fetcher_factory import FetcherFactory
from app.infrastructure.fetchers.github.github_fetcher_adapter import GithubFetcherAdapter

@pytest.fixture(autouse=True)
def set_github_env(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    monkeypatch.setenv("GITHUB_REPO", "test-owner/test-repo")

def test_create_fetcher_github():
    fetcher = FetcherFactory.create_fetcher("github")
    assert isinstance(fetcher, GithubFetcherAdapter)

def test_create_fetcher_unsupported():
    with pytest.raises(ValueError):
        FetcherFactory.create_fetcher("unknown")

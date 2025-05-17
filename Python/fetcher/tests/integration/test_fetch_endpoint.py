import os
os.environ["GITHUB_TOKEN"] = "fake-token"
os.environ["GITHUB_REPO"] = "fake/repo"

from fastapi.testclient import TestClient
import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock
from app.main import app
from app.application.services.fetcher_service import FetcherService
from app.config.dependencies.services import get_fetcher_service


@pytest.fixture
def override_fetcher_service():
    fake_fetcher = MagicMock()
    fake_fetcher.default_per_page = 5
    fake_fetcher.fetch = AsyncMock(return_value=[
        {
            "sha": "abc1",
            "author": {"login": "Alice"},
            "commit": {"author": {"date": "2024-01-01T10:00:00Z"}}
        },
        {
            "sha": "abc2",
            "author": {"login": "Bob"},
            "commit": {"author": {"date": "2024-01-01T11:00:00Z"}}
        }
    ])

    mock_factory = MagicMock()
    mock_factory.create_fetcher.return_value = fake_fetcher

    mock_author_service = MagicMock()
    mock_author_service.manage_authors = AsyncMock(return_value={
        "Alice": uuid.uuid4(),
        "Bob": uuid.uuid4()
    })

    mock_commit_service = MagicMock()
    mock_commit_service.process_and_store_commits = AsyncMock(return_value=2)

    mock_logger = MagicMock()

    return FetcherService(
        fetcher_factory=mock_factory,
        author_service=mock_author_service,
        commit_service=mock_commit_service,
        logger=mock_logger
    )


def test_fetch_commits_endpoint_success(override_fetcher_service):
    app.dependency_overrides[get_fetcher_service] = lambda: override_fetcher_service

    with TestClient(app) as client:
        response = client.post("/api/v1/fetching/fetch", json={"count": 5})

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "commits fetching successfully"
    assert data["stored_commits"] == 2

    app.dependency_overrides.clear()


def test_fetch_commits_missing_count():
    with TestClient(app) as client:
        response = client.post("/api/v1/fetching/fetch", json={})

    assert response.status_code == 422



def test_fetch_commits_internal_server_error(monkeypatch):
    broken_service = MagicMock()
    broken_service.fetch_and_store_commits = AsyncMock(side_effect=Exception("Something went wrong"))

    app.dependency_overrides[get_fetcher_service] = lambda: broken_service

    with TestClient(app) as client:
        response = client.post("/api/v1/fetching/fetch", json={"count": 5})

    assert response.status_code == 500
    assert "Internal server error" in response.text

    app.dependency_overrides.clear()



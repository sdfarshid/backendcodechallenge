import os
os.environ["GITHUB_TOKEN"] = "fake-token"
os.environ["GITHUB_REPO"] = "fake/repo"


import pytest
from httpx import AsyncClient
from uuid import uuid4
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from app.main import app
from app.application.services.commit_service import CommitService
from app.domain.entities.commit import Commit
from app.config.dependencies.services import get_commit_service


@pytest.fixture
def fake_commit_service():
    mock_service = AsyncMock(spec=CommitService)
    mock_service.get_commit.return_value = [
        Commit(hash="abc123", author_id=uuid4()),
        Commit(hash="def456", author_id=uuid4()),
    ]
    return mock_service


@pytest.mark.asyncio
async def test_get_commits_success(fake_commit_service):
    app.dependency_overrides[get_commit_service] = lambda: fake_commit_service


    with TestClient(app) as client:
        response = client.get("/api/v1/commit/list",  params={"page": 1, "per_page": 10})


    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_commits_empty(fake_commit_service):
    fake_commit_service.get_commit.return_value = []
    app.dependency_overrides[get_commit_service] = lambda: fake_commit_service

    with TestClient(app) as client:
        response = client.get("/api/v1/commit/list", params={"page": 1, "per_page": 10})

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_commits_with_author_id(fake_commit_service):
    author_id = uuid4()
    fake_commit_service.get_commit.return_value = [
        Commit(hash="xyz789", author_id=author_id)
    ]
    app.dependency_overrides[get_commit_service] = lambda: fake_commit_service

    with TestClient(app) as client:
        response = client.get("/api/v1/commit/list",  params={"author_id": str(author_id)})


    assert response.status_code == 200
    assert response.json()[0]["hash"] == "xyz789"

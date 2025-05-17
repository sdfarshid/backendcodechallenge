import os


os.environ["GITHUB_TOKEN"] = "fake-token"
os.environ["GITHUB_REPO"] = "fake/repo"


import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.application.services.author_service import AuthorService
from app.domain.aggregates.author import Author
from app.config.dependencies.services import get_author_service


@pytest.fixture
def fake_author_service():
    mock_service = AsyncMock(spec=AuthorService)
    mock_service.list_authors.return_value = [
        Author(name="Alice"),
        Author(name="Bob"),
    ]
    return mock_service


@pytest.mark.asyncio
async def test_get_authors_success(fake_author_service):
    app.dependency_overrides[get_author_service] = lambda: fake_author_service

    with TestClient(app) as client:
        response = client.get("/api/v1/author/list",  params={"page": 1, "per_page": 10})

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_authors_empty(fake_author_service):
    fake_author_service.list_authors.return_value = []
    app.dependency_overrides[get_author_service] = lambda: fake_author_service

    with TestClient(app) as client:
        response = client.get("/api/v1/author/list",  params={"page": 1, "per_page": 10})

    assert response.status_code == 200
    assert response.json() == []

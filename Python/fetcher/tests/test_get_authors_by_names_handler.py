import os

from app.domain.interface.Iauthor_repository import IAuthorRepository

os.environ["GITHUB_TOKEN"] = "fake-token"
os.environ["GITHUB_REPO"] = "fake/repo"


from unittest.mock import MagicMock, AsyncMock
from app.application.handlers.get_author_by_names import GetAuthorsByNamesCommandHandler
from app.application.queries.get_authors_by_name import GetAuthorsByNamesQuery
from app.domain.aggregates.author import Author

import uuid
import pytest


@pytest.fixture
async def mock_author_repo():
    repo = AsyncMock(spec=IAuthorRepository)
    return repo

@pytest.mark.asyncio
async def test_get_authors_by_names_success():
    fake_authors = [
        Author(name="author1", id=uuid.uuid4()),
        Author(name="author2", id=uuid.uuid4())
    ]

    mock_repo = MagicMock()
    mock_repo.get_authors_by_names = AsyncMock(return_value=fake_authors)

    handler = GetAuthorsByNamesCommandHandler(mock_repo, MagicMock())

    query = GetAuthorsByNamesQuery(unique_author_names=["author1", "author2"])
    result = await handler.handle(query)

    assert len(result) == 2
    assert result["author1"] == fake_authors[0].id
    assert result["author2"] == fake_authors[1].id
    mock_repo.get_authors_by_names.assert_awaited_once_with(["author1", "author2"])


@pytest.mark.asyncio
async def test_get_authors_by_names_no_match():
    mock_repo = MagicMock()
    mock_repo.get_authors_by_names = AsyncMock(return_value=[])

    handler = GetAuthorsByNamesCommandHandler(mock_repo, MagicMock())

    query = GetAuthorsByNamesQuery(unique_author_names=["nonexistent"])
    result = await handler.handle(query)

    assert result == {}
    mock_repo.get_authors_by_names.assert_awaited_once_with(["nonexistent"])


@pytest.mark.asyncio
async def test_get_authors_by_names_empty_input():
    mock_repo = MagicMock()
    mock_repo.get_authors_by_names = AsyncMock(return_value=[])

    handler = GetAuthorsByNamesCommandHandler(mock_repo, MagicMock())

    query = GetAuthorsByNamesQuery(unique_author_names=[])
    result = await handler.handle(query)

    assert result == {}
    mock_repo.get_authors_by_names.assert_awaited_once_with([])

@pytest.mark.asyncio
async def test_get_authors_by_names_raises_exception():
    mock_repo = MagicMock()
    mock_repo.get_authors_by_names = AsyncMock(side_effect=Exception("DB failure"))

    handler = GetAuthorsByNamesCommandHandler(mock_repo, MagicMock())

    query = GetAuthorsByNamesQuery(unique_author_names=["authorX"])

    with pytest.raises(RuntimeError) as exc_info:
        await handler.handle(query)

    assert "Failed fetching users" in str(exc_info.value)
    mock_repo.get_authors_by_names.assert_awaited_once_with(["authorX"])


@pytest.mark.asyncio
async def test_get_authors_by_names_duplicate_input():
    id1 = uuid.uuid4()
    author = Author(name="author1", id=id1)

    mock_repo = MagicMock()
    mock_repo.get_authors_by_names = AsyncMock(return_value=[author])

    handler = GetAuthorsByNamesCommandHandler(mock_repo, MagicMock())

    query = GetAuthorsByNamesQuery(unique_author_names=["author1", "author1"])
    result = await handler.handle(query)

    assert result == {"author1": id1}
    mock_repo.get_authors_by_names.assert_awaited_once_with(["author1", "author1"])

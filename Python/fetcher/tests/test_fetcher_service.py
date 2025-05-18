
from app.utilities.log import fetcher_logger

import uuid
import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock

from app.application.commands.fetch_commits import FetchCommitsCommand
from app.application.services.fetcher_service import FetcherService




def make_commit(sha, login, date="2024-01-01T12:00:00Z"):
    return {
        "sha": sha,
        "author": {"login": login} if login else None,
        "commit": {"author": {"date": date}}
    }


def make_fake_fetcher(per_page=5, side_effect=None):
    fake_fetcher = MagicMock()
    fake_fetcher.default_per_page = per_page
    fake_fetcher.fetch = AsyncMock(side_effect=side_effect)
    return fake_fetcher


@pytest.mark.asyncio
async def test_fetch_and_store_commits_parallel():
    fake_commits_page_1 = [make_commit("sha1", "Alice"), make_commit("sha2", "Bob"), make_commit("sha3", "Alice")]
    fake_commits_page_2 = [make_commit("sha4", "Charlie"), make_commit("sha5", "Bob")]

    fake_fetcher = make_fake_fetcher(side_effect=[fake_commits_page_1, fake_commits_page_2])
    mock_factory = MagicMock()
    mock_factory.create_fetcher.return_value = fake_fetcher

    uuid_alice, uuid_bob, uuid_charlie = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()

    author_service = MagicMock()
    author_service.manage_authors = AsyncMock(return_value={
        "Alice": uuid_alice,
        "Bob": uuid_bob,
        "Charlie": uuid_charlie
    })

    commit_service = MagicMock()
    commit_service.process_and_store_commits = AsyncMock(return_value=5)

    service = FetcherService(
        fetcher_factory=mock_factory,
        author_service=author_service,
        commit_service=commit_service,
        logger=fetcher_logger
    )

    command = FetchCommitsCommand(count=10)
    result = await service.fetch_and_store_commits(command)

    assert result["message"] == "commits fetching successfully"
    assert result["stored_commits"] == 5
    assert fake_fetcher.fetch.await_count == 2


@pytest.mark.asyncio
async def test_fetch_and_store_commits_fetcher_partial_failure(caplog):
    async def fake_fetch(page):
        if page == 2:
            raise Exception("API error")
        return [make_commit("sha", "Alice")]

    fake_fetcher = make_fake_fetcher(side_effect=fake_fetch)
    mock_factory = MagicMock()
    mock_factory.create_fetcher.return_value = fake_fetcher

    author_service = MagicMock()
    author_service.manage_authors = AsyncMock(return_value={"Alice": uuid.uuid4()})

    commit_service = MagicMock()
    commit_service.process_and_store_commits = AsyncMock(return_value=1)

    service = FetcherService(
        fetcher_factory=mock_factory,
        author_service=author_service,
        commit_service=commit_service,
        logger=fetcher_logger
    )

    command = FetchCommitsCommand(count=10)
    result = await service.fetch_and_store_commits(command)

    assert result["stored_commits"] == 1
    assert fake_fetcher.fetch.await_count == 2
    assert "API error" in caplog.text


@pytest.mark.asyncio
async def test_fetch_and_store_commits_author_handler_fails():
    fake_fetcher = make_fake_fetcher(side_effect=[[make_commit("sha", "Alice")]])
    mock_factory = MagicMock()
    mock_factory.create_fetcher.return_value = fake_fetcher

    author_service = MagicMock()
    author_service.manage_authors = AsyncMock(side_effect=Exception("DB down"))

    commit_service = MagicMock()

    service = FetcherService(
        fetcher_factory=mock_factory,
        author_service=author_service,
        commit_service=commit_service,
        logger=fetcher_logger
    )

    with pytest.raises(Exception) as e:
        await service.fetch_and_store_commits(FetchCommitsCommand(count=5))

    assert "DB down" in str(e.value)


@pytest.mark.asyncio
async def test_fetch_and_store_commits_store_commits_fails():
    fake_fetcher = make_fake_fetcher(side_effect=[[make_commit("sha", "Alice")]])
    mock_factory = MagicMock()
    mock_factory.create_fetcher.return_value = fake_fetcher

    author_service = MagicMock()
    author_service.manage_authors = AsyncMock(return_value={"Alice": uuid.uuid4()})

    commit_service = MagicMock()
    commit_service.process_and_store_commits = AsyncMock(side_effect=Exception("Storage failed"))

    service = FetcherService(
        fetcher_factory=mock_factory,
        author_service=author_service,
        commit_service=commit_service,
        logger=fetcher_logger
    )

    with pytest.raises(Exception) as e:
        await service.fetch_and_store_commits(FetchCommitsCommand(count=5))

    assert "Storage failed" in str(e.value)

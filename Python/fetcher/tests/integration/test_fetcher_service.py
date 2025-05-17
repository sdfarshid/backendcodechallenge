import os
import uuid

os.environ["GITHUB_TOKEN"] = "fake-token"
os.environ["GITHUB_REPO"] = "fake/repo"


from unittest.mock import MagicMock, AsyncMock

import pytest

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
    fake_commits_page_1 = [
        make_commit("sha1", "Alice"),
        make_commit("sha2", "Bob"),
        make_commit("sha3", "Alice")
    ]

    fake_commits_page_2 = [
        make_commit("sha4", "Charlie"),
        make_commit("sha5", "Bob")
    ]

    fake_fetcher = make_fake_fetcher(side_effect=[fake_commits_page_1, fake_commits_page_2])






@pytest.mark.asyncio
async def test_fetch_and_store_commits_parallel():

    fake_commits_page_1 = [
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
    ]
    fake_commits_page_2 = [
        {
            "sha": "abc3",
            "author": {"login": "Charlie"},
            "commit": {"author": {"date": "2024-01-01T12:00:00Z"}}
        },
        {
            "sha": "abc4",
            "author": {"login": "Bob"},
            "commit": {"author": {"date": "2024-01-01T13:00:00Z"}}
        }
    ]

    fake_fetcher = MagicMock()
    fake_fetcher.default_per_page = 5
    fake_fetcher.fetch = AsyncMock(side_effect=[fake_commits_page_1, fake_commits_page_2])

    mock_fetcher_factory = MagicMock()
    mock_fetcher_factory.create_fetcher.return_value = fake_fetcher

    uuid_alice = uuid.uuid4()
    uuid_bob = uuid.uuid4()
    uuid_charlie = uuid.uuid4()




    mock_author_handler = MagicMock()
    mock_author_handler.handle = AsyncMock(
        return_value={
            "Alice": uuid_alice,
            "Bob": uuid_bob,
            "Charlie":  uuid_charlie 
        }
    )

    mock_create_author_handler = MagicMock()
    mock_create_author_handler.handle = AsyncMock(return_value={
        "Alice": uuid_alice,
        "Bob": uuid_bob,
        "Charlie":  uuid_charlie 
    })


    mock_store_commits_handler = MagicMock()
    mock_store_commits_handler.handle = AsyncMock(return_value=5)


    service = FetcherService(
        get_author_by_name_handler=mock_author_handler,
        create_author_handler=mock_create_author_handler,
        store_commits_handler=mock_store_commits_handler,
        fetcher_factory=mock_fetcher_factory
    )

    command = FetchCommitsCommand(count=10)
    result = await service.fetch_and_store_commits(command)

    assert result["message"] == "commits fetching successfully"
    assert result["stored_commits"] == 5
    assert fake_fetcher.fetch.await_count == 2
    mock_store_commits_handler.handle.assert_awaited_once()




@pytest.mark.asyncio
async def test_fetch_and_store_commits_fetcher_partial_failure(caplog):
    """
        When during a fetching one request of pages throw exception
    """

    fake_commits_page_1 = [
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
    ]


    async def fake_fetch(page, per_page):
        if page == 2:
            raise Exception("API error")
        return fake_commits_page_1

    fake_fetcher = MagicMock()
    fake_fetcher.default_per_page = 5
    fake_fetcher.fetch = AsyncMock(side_effect=fake_fetch)

    mock_factory = MagicMock()
    mock_factory.create_fetcher.return_value = fake_fetcher

    mock_author_handler = MagicMock()
    mock_author_handler.handle = AsyncMock(return_value={"Alice": uuid.uuid4()})
    mock_create_handler = MagicMock()
    mock_create_handler.handle = AsyncMock(return_value={"Alice": uuid.uuid4()})
    mock_store_handler = MagicMock()
    mock_store_handler.handle = AsyncMock(return_value=1)

    service = FetcherService(
        get_author_by_name_handler=mock_author_handler,
        create_author_handler=mock_create_handler,
        store_commits_handler=mock_store_handler,
        fetcher_factory=mock_factory
    )

    command = FetchCommitsCommand(count=10)
    result = await service.fetch_and_store_commits(command)

    assert result["stored_commits"] == 1
    assert fake_fetcher.fetch.await_count == 2
    assert "API error" in caplog.text


@pytest.mark.asyncio
async def test_fetch_and_store_commits_author_handler_fails():
    fake_fetcher = MagicMock()
    fake_fetcher.default_per_page = 5
    fake_fetcher.fetch = AsyncMock(return_value=[{"author": "Alice"}])

    mock_factory = MagicMock()
    mock_factory.create_fetcher.return_value = fake_fetcher

    failing_author_handler = MagicMock()
    failing_author_handler.handle = AsyncMock(side_effect=Exception("DB down"))

    service = FetcherService(
        get_author_by_name_handler=failing_author_handler,
        create_author_handler=MagicMock(),
        store_commits_handler=MagicMock(),
        fetcher_factory=mock_factory
    )

    command = FetchCommitsCommand(count=5)
    with pytest.raises(Exception) as e:
        await service.fetch_and_store_commits(command)

    assert "DB down" in str(e.value)




@pytest.mark.asyncio
async def test_fetch_and_store_commits_store_commits_fails():
    fake_fetcher = MagicMock()
    fake_fetcher.default_per_page = 5
    fake_fetcher.fetch = AsyncMock(return_value=[{"author": "Alice"}])

    mock_factory = MagicMock()
    mock_factory.create_fetcher.return_value = fake_fetcher

    mock_author_handler = MagicMock()
    mock_author_handler.handle = AsyncMock(return_value={"Alice": uuid.uuid4()})
    mock_create_handler = MagicMock()
    mock_create_handler.handle = AsyncMock(return_value={"Alice": uuid.uuid4()})
    failing_store_handler = MagicMock()
    failing_store_handler.handle = AsyncMock(side_effect=Exception("Storage failed"))

    service = FetcherService(
        get_author_by_name_handler=mock_author_handler,
        create_author_handler=mock_create_handler,
        store_commits_handler=failing_store_handler,
        fetcher_factory=mock_factory
    )

    command = FetchCommitsCommand(count=5)
    with pytest.raises(Exception) as e:
        await service.fetch_and_store_commits(command)

    assert "Storage failed" in str(e.value)



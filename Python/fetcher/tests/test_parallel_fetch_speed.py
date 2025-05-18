
from app.application.commands.fetch_commits import FetchCommitsCommand



import asyncio
import time
from unittest.mock import MagicMock, AsyncMock

import pytest

from app.application.services.fetcher_service import FetcherService




@pytest.mark.asyncio
async def test_parallel_fetch_speed(monkeypatch):
    fake_fetcher = MagicMock()
    fake_fetcher.default_per_page = 1

    async def slow_fetch(per_page, page):
        await asyncio.sleep(1)
        return [{"author": f"user{page}"}]

    fake_fetcher.fetch = AsyncMock(side_effect=slow_fetch)

    mock_factory = MagicMock()
    mock_factory.create_fetcher.return_value = fake_fetcher

    service = FetcherService(
        author_service=AsyncMock(),
        commit_service=AsyncMock(),
        logger=MagicMock(),
        fetcher_factory=mock_factory
    )
    start = time.perf_counter()
    await service._parallel_fetching(FetchCommitsCommand(count=5))
    duration = time.perf_counter() - start

    assert duration < 3

@pytest.mark.asyncio
async def test_parallel_fetch_partial_failure():
    fake_fetcher = MagicMock()
    fake_fetcher.default_per_page = 1

    async def maybe_fail(page):
        if page == 3:
            raise Exception("Page 3 failed")
        await asyncio.sleep(0.1)
        return [{"author": f"user{page}"}]

    fake_fetcher.fetch = AsyncMock(side_effect=maybe_fail)

    mock_factory = MagicMock()
    mock_factory.create_fetcher.return_value = fake_fetcher

    service = FetcherService(
        author_service=AsyncMock(),
        commit_service=AsyncMock(),
        logger=MagicMock(),
        fetcher_factory=mock_factory
    )

    command = FetchCommitsCommand(count=5)
    result = await service._parallel_fetching(command)

    assert len(result) == 5
    non_empty_lists = []
    for result_row in result:
        if isinstance(result_row, list) and len(result_row) > 0:
            non_empty_lists.append(result_row)

    assert len(non_empty_lists) == 4


@pytest.mark.asyncio
async def test_parallel_fetch_all_failures():
    fake_fetcher = MagicMock()
    fake_fetcher.default_per_page = 1

    async def always_fail(per_page, page):
        raise Exception(f"Failing page {page}")

    fake_fetcher.fetch = AsyncMock(side_effect=always_fail)

    mock_factory = MagicMock()
    mock_factory.create_fetcher.return_value = fake_fetcher

    service = FetcherService(
        author_service=AsyncMock(),
        commit_service=AsyncMock(),
        logger=MagicMock(),
        fetcher_factory=mock_factory
    )

    command = FetchCommitsCommand(count=3)
    result = await service._parallel_fetching(command)

    assert result == [[], [], []]





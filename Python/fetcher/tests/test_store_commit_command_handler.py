import os
import datetime
import uuid
import pytest
import pytest_asyncio
from unittest.mock import MagicMock, AsyncMock

from app.application.commands.store_commits import StoreCommitsCommand
from app.application.handlers.store_commits import StoreCommitsCommandHandler
from app.domain.entities.commit import Commit

os.environ["GITHUB_TOKEN"] = "fake-token"
os.environ["GITHUB_REPO"] = "fake/repo"

def fake_commit(hash_value: str) -> dict:
    return {
        "hash": hash_value,
        "created_at": datetime.datetime.utcnow()
    }

@pytest_asyncio.fixture
async def mock_handler():
    mock_repo = MagicMock()
    mock_logger = MagicMock()
    mock_repo.add_commits_batch = AsyncMock()
    return StoreCommitsCommandHandler(mock_repo, mock_logger), mock_repo

@pytest.mark.asyncio
async def test_store_commits_success(mock_handler):
    handler, mock_repo = mock_handler

    author_id1 = uuid.uuid4()
    author_id2 = uuid.uuid4()

    fake_command = StoreCommitsCommand(
        grouped_commits={
            author_id1: [fake_commit("hash1"), fake_commit("hash2")],
            author_id2: [fake_commit("hash3")],
        }
    )

    await handler.handle(fake_command)

    mock_repo.add_commits_batch.assert_awaited_once()
    args, _ = mock_repo.add_commits_batch.call_args
    stored_commits = args[0]

    assert len(stored_commits) == 3
    assert {c.hash for c in stored_commits} == {"hash1", "hash2", "hash3"}

@pytest.mark.asyncio
async def test_store_commits_ignores_duplicates(mock_handler):
    handler, mock_repo = mock_handler

    author_id = uuid.uuid4()
    fake_command = StoreCommitsCommand(
        grouped_commits={
            author_id: [fake_commit("same_hash"), fake_commit("same_hash")]
        }
    )

    await handler.handle(fake_command)

    args, _ = mock_repo.add_commits_batch.call_args
    stored_commits = args[0]

    assert len(stored_commits) == 1
    assert stored_commits[0].hash == "same_hash"

@pytest.mark.asyncio
async def test_store_commits_empty_input(mock_handler):
    handler, mock_repo = mock_handler

    fake_command = StoreCommitsCommand(grouped_commits={})
    await handler.handle(fake_command)

    mock_repo.add_commits_batch.assert_awaited_once_with([])

@pytest.mark.asyncio
async def test_store_commits_raises_exception():
    mock_repo = MagicMock()
    mock_logger = MagicMock()
    mock_repo.add_commits_batch = AsyncMock(side_effect=Exception("DB error"))

    handler = StoreCommitsCommandHandler(mock_repo, mock_logger)

    author_id = uuid.uuid4()
    fake_command = StoreCommitsCommand(
        grouped_commits={author_id: [fake_commit("hash1")]}
    )

    with pytest.raises(RuntimeError) as exc_info:
        await handler.handle(fake_command)

    assert "Failed to store commits" in str(exc_info.value)
    mock_repo.add_commits_batch.assert_awaited_once()

@pytest.mark.asyncio
async def test_store_commits_with_duplicate_hashes(mock_handler):
    handler, mock_repo = mock_handler

    author_id = uuid.uuid4()
    fake_command = StoreCommitsCommand(
        grouped_commits={
            author_id: [
                fake_commit("abc123"),
                fake_commit("abc123"),
                fake_commit("xyz456")
            ]
        }
    )

    await handler.handle(fake_command)

    args, _ = mock_repo.add_commits_batch.call_args
    passed_commits = args[0]

    assert len(passed_commits) == 2
    hashes = [c.hash for c in passed_commits]
    assert "abc123" in hashes
    assert "xyz456" in hashes

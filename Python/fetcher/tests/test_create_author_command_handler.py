from unittest.mock import MagicMock, AsyncMock


import uuid
import pytest
from app.application.commands.crete_author import CreateAuthorCommand
from app.application.handlers.create_author import CreateAuthorCommandHandler


@pytest.fixture
def handler_with_mock_repo():
    mock_repo = MagicMock()
    mock_repo.add_author = AsyncMock()
    mock_logger = MagicMock()
    return CreateAuthorCommandHandler(mock_repo, mock_logger), mock_repo


@pytest.mark.asyncio
async def test_create_author_command_handler(handler_with_mock_repo):

    handler, mock_repo = handler_with_mock_repo

    fake_command = CreateAuthorCommand(
        unique_author_names=["author1", "author2"],
        existing_author_map={}
    )

    result = await handler.handle(fake_command)

    assert len(result) == 2
    assert "author1" in result
    assert "author2" in result
    assert isinstance(result["author1"], uuid.UUID)
    mock_repo.add_author.assert_awaited()

@pytest.mark.asyncio
async def test_create_unique_author_command_handler(handler_with_mock_repo):
    handler, mock_repo = handler_with_mock_repo
    existing_id = uuid.uuid4()
    fake_command = CreateAuthorCommand(
        unique_author_names=["author1", "author2"],
        existing_author_map={"author1": existing_id}
    )

    result = await handler.handle(fake_command)

    assert "author1" in result
    assert result["author1"] == existing_id
    assert "author2" in result
    assert isinstance(result["author2"], uuid.UUID)
    assert len(result) == 2
    mock_repo.add_author.assert_awaited_once()

@pytest.mark.asyncio
async def test_create_author_command_handler_duplicate_names_in_unique_list(handler_with_mock_repo):
    handler, mock_repo = handler_with_mock_repo

    fake_command = CreateAuthorCommand(
        unique_author_names=["author1", "author1", "author2"],
        existing_author_map={}
    )

    result = await handler.handle(fake_command)

    assert len(result) == 2
    assert "author1" in result
    assert "author2" in result
    assert isinstance(result["author1"], uuid.UUID)
    assert isinstance(result["author2"], uuid.UUID)

    assert mock_repo.add_author.await_count == 2


@pytest.mark.asyncio
async def test_create_author_command_handler_all_duplicates(handler_with_mock_repo):
    handler, mock_repo = handler_with_mock_repo


    existing_map = {
        "author1": uuid.uuid4(),
        "author2": uuid.uuid4()
    }

    fake_command = CreateAuthorCommand(
        unique_author_names=["author1", "author2"],
        existing_author_map=existing_map.copy()
    )

    result = await handler.handle(fake_command)

    assert result == existing_map

@pytest.mark.asyncio
async def test_create_author_command_handler_empty_list(handler_with_mock_repo):
    handler, mock_repo = handler_with_mock_repo


    fake_command = CreateAuthorCommand(
        unique_author_names=[],
        existing_author_map={}
    )

    result = await handler.handle(fake_command)
    assert result == {}

@pytest.mark.asyncio
async def test_create_author_command_handler_raises_on_add_error():
    mock_repo = MagicMock()
    mock_repo.add_author = AsyncMock(side_effect=Exception("DB error"))
    handler = CreateAuthorCommandHandler(mock_repo,MagicMock())

    fake_command = CreateAuthorCommand(
        unique_author_names=["authorX"],
        existing_author_map={}
    )


    with pytest.raises(RuntimeError) as exc_info:
        await handler.handle(fake_command)

    assert "Failed storing authors" in str(exc_info.value)
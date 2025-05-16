from __future__ import annotations

from typing import List
from uuid import UUID, uuid4

from fastapi import Depends
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.mixins.pagination import PaginationParams
from app.domain.entities.commit import Commit
from app.domain.interface.Icommit_repository import ICommitRepository
from app.infrastructure.database.models.commit import CommitModel
from app.infrastructure.database.session import get_db
from sqlalchemy import select

from app.infrastructure.mapper.mapper import mapper
from app.utilities.log import DebugError


class CommitRepository(ICommitRepository):


    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def add_commits_batch(self, commits: List[Commit]) -> None:

        values = [{
            "id": commit.id if commit.id else uuid4(),
            "hash": commit.hash,
            "author_id": commit.author_id
        } for commit in commits]

        stmt = insert(CommitModel).values(values)
        stmt = stmt.on_conflict_do_nothing(index_elements=["hash"])

        try:
            await self.db.execute(stmt)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            DebugError(f"PostgresSQL batch insert failed: {e}")
            raise


    async def get_commit_by_author_id(self, author_id: UUID, pagination: PaginationParams) -> List[Commit] | None:
        try:
            stmt = select(CommitModel).where(CommitModel.author_id == author_id)
            result = await self.db.execute(stmt)
            rows_model = result.scalars().one_or_none()

            if rows_model is None:
                return None

            return mapper.commit_db_to_domain_model(rows_model)

        except SQLAlchemyError as e:
            DebugError(f" AuthorRepository - get_author_by_name :  {e}")
            raise RuntimeError(f"Database error while fetching author by name: {e}") from e




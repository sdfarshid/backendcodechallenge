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


    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_commits_batch(self, commits: List[Commit]) -> int:

        values = [{
            "id": commit.id if commit.id else uuid4(),
            "hash": commit.hash,
            "author_id": commit.author_id
        } for commit in commits]

        stmt = (
            insert(CommitModel)
            .values(values)
            .on_conflict_do_nothing(index_elements=["hash"])
            .returning(CommitModel.id)
        )

        try:
            result = await self.db.execute(stmt)
            await self.db.commit()
            inserted_ids = result.scalars().all()
            return len(inserted_ids)
        except Exception as e:
            await self.db.rollback()
            DebugError(f"PostgresSQL batch insert failed: {e}")
            raise



    async def list_commits(self, pagination: PaginationParams, author_id: [UUID, None]) -> List[Commit] | None:
        try:
            query = select(CommitModel)
            if author_id:
                query = query.where(CommitModel.author_id == author_id)

            query = query.offset(pagination.offset).limit(pagination.limit)

            result = await self.db.execute(query)
            rows_model = result.scalars().all()

            if rows_model is None:
                return None

            return [mapper.commit_db_to_domain_model(commit) for commit in rows_model]

        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error while fetching lis of  commits: {e}") from e


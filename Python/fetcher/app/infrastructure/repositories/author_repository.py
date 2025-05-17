from __future__ import annotations

from typing import List

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.mixins.pagination import PaginationParams
from app.domain.aggregates.author import Author
from app.domain.interface.Iauthor_repository import IAuthorRepository
from app.infrastructure.database.models.author import AuthorModel
from app.infrastructure.database.session import get_db
from sqlalchemy import select

from app.infrastructure.mapper.mapper import mapper
from app.utilities.log import DebugError


class AuthorRepository(IAuthorRepository):


    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_author(self, author: Author) -> Author:
        try:
            author_db =  mapper.author_model_to_db_model(author)
            self.db.add(author_db)
            await self.db.commit()
            await self.db.refresh(author_db)
            return author_db
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_author_by_name(self, name: str) -> Author | None:
        try:
            stmt = select(AuthorModel).where(AuthorModel.name == name)
            result = await self.db.execute(stmt)
            author_model = result.scalars().one_or_none()

            if author_model is None:
                return None

            return mapper.author_db_to_domain_model(author_model)

        except SQLAlchemyError as e:
            DebugError(f" AuthorRepository - get_author_by_name :  {e}")
            raise RuntimeError(f"Database error while fetching author by name: {e}") from e

    async def get_authors_by_names(self, names: list[str]) -> List[Author] | None:
        try:
            stmt = select(AuthorModel).where(AuthorModel.name.in_(names))
            result = await self.db.execute(stmt)
            author_models = result.scalars().all()

            return [mapper.author_db_to_domain_model(author) for author in author_models]

        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error while fetching authors by names: {e}") from e


    async def list_authors(self, pagination: PaginationParams) -> List[Author] | None:
        try:
            result = await self.db.execute(
                select(AuthorModel).offset(pagination.offset).limit(pagination.limit)
            )
            authors_model =  result.scalars().all()

            return [mapper.author_db_to_domain_model(author) for author in authors_model]

        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error while fetching authors : {e}") from e



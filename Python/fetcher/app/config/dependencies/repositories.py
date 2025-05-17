from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.repositories.author_repository import AuthorRepository
from app.infrastructure.repositories.commit_repository import CommitRepository
from app.infrastructure.database.session import get_db

def get_author_repository(db: AsyncSession = Depends(get_db)) -> AuthorRepository:
    return AuthorRepository(db)

def get_commit_repository(db: AsyncSession = Depends(get_db)) -> CommitRepository:
    return CommitRepository(db)

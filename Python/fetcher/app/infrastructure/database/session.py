import logging
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.config import settings


logger = logging.getLogger(__name__)


try:
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    logger.info("Database engine created successfully")
except Exception as e:
    logger.critical(f"Database connection failed: {str(e)}")
    raise


AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[Any, Any]:
    async with AsyncSessionLocal() as session:
        yield session



async def init_db():
    await create_all_tables()


async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("All tables created successfully")

import asyncio
import os
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from app.infrastructure.database.session import Base
from app.config.config import get_settings

from app.infrastructure.database.models.author import AuthorModel
from app.infrastructure.database.models.commit import CommitModel


# Config file parser
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Load DB URL from env or settings
DATABASE_URL = os.getenv("DATABASE_URL", get_settings().DATABASE_URL)
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# For autogenerate support
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Apply migration logic."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(DATABASE_URL, future=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())

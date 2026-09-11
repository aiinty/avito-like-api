from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import config


postgres_engine = create_async_engine(config.async_postgres_connect_url, echo=True)

postgres_make_session = async_sessionmaker(postgres_engine, expire_on_commit=False)

async def postgres_create_all():
    async with postgres_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def postgres_drop_all():
    async with postgres_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        
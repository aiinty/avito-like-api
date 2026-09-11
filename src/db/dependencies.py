from src.db.postgres import postgres_make_session


async def get_postgres_session():
    """Make async session."""

    async with postgres_make_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise

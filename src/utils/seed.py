import asyncio
from sqlmodel import select
from src.db.postgres import postgres_make_session
from src.modules.categories.models import Category
from src.modules.users.models import User
from src.modules.items.models import Item
from src.modules.messages.models import Message


async def seed():
    async with postgres_make_session() as session:
        result = await session.execute(
            select(Category)
        )

        if result.first():
            return

        session.add_all([
            Category(name="Электроника", emoji="💻"),
            Category(name="Одежда", emoji="👕"),
            Category(name="Автомобили", emoji="🚘"),
        ])

        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())
    
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
            Category(name="Недвижимость", emoji="🏠"),
            Category(name="Дом и сад", emoji="🛋️"),
            Category(name="Бытовая техника", emoji="🔌"),
            Category(name="Детские товары", emoji="🧸"),
            Category(name="Хобби и отдых", emoji="🎮"),
            Category(name="Спорт", emoji="⚽"),
            Category(name="Животные", emoji="🐾"),
            Category(name="Услуги", emoji="🛠️"),
            Category(name="Работа", emoji="💼"),
            Category(name="Запчасти", emoji="⚙️"),
            Category(name="Строительство и ремонт", emoji="🔨"),
            Category(name="Красота и здоровье", emoji="💄"),
            Category(name="Книги", emoji="📚"),
            Category(name="Прочее", emoji="📦"),
        ])

        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())
    
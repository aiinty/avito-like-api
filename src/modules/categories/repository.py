from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.modules.categories.models import Category


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, category_id: int) -> Category | None:
        query = (
            select(Category).where(Category.id == category_id)
        )

        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def get_all(self) -> Sequence[Category]:
        query = (
            select(Category).order_by(Category.id.desc())    
        )

        result = await self.session.execute(query)
        return result.scalars().all()

from typing import Any, Sequence
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import func, select
from src.modules.items.models import Item
from src.modules.items.schemas import ItemCreate


class ItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, item_id: int) -> Item | None:
        query = (
            select(Item)
            .options(
                selectinload(Item.author),
                selectinload(Item.category),
            )
            .where(Item.id == item_id)
        )

        result = await self.session.execute(query)
        return result.scalars().first()

    async def count_all(
        self,
        category_id: int | None = None,
        author_id: UUID | None = None,
    ) -> int:
        query = select(func.count(Item.id))

        if category_id is not None:
            query = query.where(Item.category_id == category_id)

        if author_id is not None:
            query = query.where(Item.author_id == author_id)

        result = await self.session.execute(query)
        return result.scalar() or 0

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 100,
        category_id: int | None = None,
        author_id: UUID | None = None,
    ) -> Sequence[Item]:
        query = (
            select(Item)
            .options(
                selectinload(Item.author),
                selectinload(Item.category),
            )
        )

        if category_id is not None:
            query = query.where(Item.category_id == category_id)

        if author_id is not None:
            query = query.where(Item.author_id == author_id)

        query = (
            query
            .order_by(Item.id.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(
        self,
        data: ItemCreate,
        author_id: UUID,
    ) -> Item:
        payload = data.model_dump()

        db_item = Item(
            **payload,
            author_id=author_id,
        )

        self.session.add(db_item)

        await self.session.flush()

        return await self.get_by_id(db_item.id)

    async def update(
        self,
        db_item: Item,
        update_data: dict[str, Any],
    ) -> Item:
        for key, value in update_data.items():
            setattr(db_item, key, value)

        self.session.add(db_item)

        await self.session.flush()

        return await self.get_by_id(db_item.id)

    async def delete(self, db_item: Item) -> None:
        await self.session.delete(db_item)
        await self.session.flush()

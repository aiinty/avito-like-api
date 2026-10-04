from typing import Sequence
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import func, select
from src.modules.messages.models import Message
from src.modules.messages.schemas import MessageCreate


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_item_id(
        self,
        item_id: int,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[Message]:
        query = (
            select(Message)
            .options(selectinload(Message.user))
            .where(Message.item_id == item_id)
            .order_by(Message.id.asc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def count_by_item_id(self, item_id: int) -> int:
        query = (
            select(func.count(Message.id))
            .where(Message.item_id == item_id)
        )

        result = await self.session.execute(query)
        return result.scalar() or 0

    async def create(
        self,
        item_id: int,
        user_id: UUID,
        data: MessageCreate,
    ) -> Message:
        message = Message(
            item_id=item_id,
            user_id=user_id,
            text=data.text,
        )

        self.session.add(message)
        await self.session.flush()

        query = (
            select(Message)
            .options(selectinload(Message.user))
            .where(Message.id == message.id)
        )

        result = await self.session.execute(query)
        return result.scalars().first()

from typing import Any, Sequence
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select
from src.modules.users.models import User
from src.modules.users.schemas import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def count_all(self) -> int:
        query = select(func.count(User.id))
        result = await self.session.execute(query)
        return result.scalar() or 0

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 100
    ) -> Sequence[User]:
        query = (
            select(User)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, data: UserCreate) -> User:
        payload = data.model_dump()
        db_user = User(**payload)
        
        self.session.add(db_user)
        await self.session.flush()
        await self.session.refresh(db_user)
        return db_user

    async def update(self, db_user: User, update_data: dict[str, Any]) -> User:
        for key, value in update_data.items():
            setattr(db_user, key, value)
        self.session.add(db_user)
        await self.session.flush()
        await self.session.refresh(db_user)
        return db_user

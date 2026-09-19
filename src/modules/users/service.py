from src.modules.users.models import User
from src.modules.users.schemas import UserCreate, UserUpdate
from src.modules.users.repository import UserRepository
from src.utils.schemas import Meta, PaginatedResponse
from src.utils.exceptions import NotFoundError,ValidationError
from uuid import UUID


class UserService():
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    async def _get_paginated_data(
        self,
        page: int, 
        page_size: int,
        search: str | None = None
    ) -> PaginatedResponse[User]:
        offset = (page - 1) * page_size
        
        items = await self.repo.get_all(
            limit=page_size, 
            offset=offset,
            search=search
        )
        total_count = await self.repo.count_all(search=search)
        
        return PaginatedResponse(
            items=items,
            meta=Meta.create(total_count, page, page_size)
        )

    async def get_all_users(self, page: int, page_size: int, search: str | None = None) -> PaginatedResponse[User]:
        return await self._get_paginated_data(page, page_size, search)

    async def get_user_by_username(self, username: str) -> User:
        user = await self.repo.get_by_username(username)
        #if not user:
        #    raise NotFoundError("User not found")
        return user

    async def get_user_by_email(self, email: str) -> User:
        user = await self.repo.get_by_email(email)
        #if not user:
        #    raise NotFoundError("User not found")
        return user

    async def get_by_id_or_raise(self, user_id: UUID) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user
    
    async def create_user(self, data: UserCreate) -> User:
        return await self.repo.create(data)
    
    async def self_update_user(self, user_id: UUID, data: UserUpdate) -> User:
        db_user = await self.get_by_id_or_raise(user_id)
        payload = data.model_dump(exclude_unset=True)

        new_username = payload.get("username")
        if new_username and new_username != db_user.username:
            if await self.repo.get_by_username(new_username):
                raise ValidationError("Username is already used")

        return await self.repo.update(db_user, payload)

from src.modules.users.models import User
from src.modules.users.schemas import TokenResponse, UserLogin, UserRegister, UserUpdate
from src.modules.users.repository import UserRepository
from src.utils.schemas import Meta, PaginatedResponse
from src.utils.security import create_access_token, create_refresh_token, get_password_hash, verify_password
from src.utils.exceptions import NotFoundError, UnauthorizedError, ValidationError
from uuid import UUID
from utils.auth import decode_token


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
        if not user:
            raise NotFoundError("User not found")
        return user

    async def get_user_by_email(self, email: str) -> User:
        user = await self.repo.get_by_email(email)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def get_by_id_or_raise(self, user_id: UUID) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def register_user(self, data: UserRegister) -> User:
        if await self.repo.get_by_email(data.email):
            raise ValidationError("Email is already registered")
            
        if await self.repo.get_by_username(data.username):
            raise ValidationError("Username is already used")

        hashed_pass = get_password_hash(data.password)
        return await self.repo.create(data, hashed_pass)
    
    async def self_update_user(self, user_id: UUID, data: UserUpdate) -> User:
        db_user = await self.get_by_id_or_raise(user_id)
        payload = data.model_dump(exclude_unset=True)

        new_username = payload.get("username")
        if new_username and new_username != db_user.username:
            if await self.repo.get_by_username(new_username):
                raise ValidationError("Username is already used")

        return await self.repo.update(db_user, payload)
    
    async def login(self, data: UserLogin) -> TokenResponse:
        user = await self.repo.get_by_email(data.email)
        
        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")

        access_token = create_access_token(user_id=str(user.id))
        refresh_token = create_refresh_token(user_id=str(user.id))

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    
    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        user = decode_token(refresh_token, expected_type="refresh")

        db_user = await self.repo.get_by_id(user.id)
        if not db_user:
            raise UnauthorizedError("Invalid token")

        new_access = create_access_token(user_id=str(user.id))
        new_refresh = create_refresh_token(user_id=str(user.id))

        return TokenResponse(access_token=new_access, refresh_token=new_refresh)

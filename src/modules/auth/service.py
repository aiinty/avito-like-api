from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4
import jwt
from src.modules.auth.models import RefreshToken
from src.modules.auth.security import decode_token,  create_access_token, create_refresh_token, get_password_hash, verify_password
from src.modules.auth.repository import RefreshTokenRepository
from src.modules.users.schemas import UserCreate
from src.modules.users.service import UserService
from src.modules.users.models import User
from src.modules.auth.schemas import TokenResponse, LoginRequest, RegisterRequest
from src.utils.exceptions import UnauthorizedError, ValidationError
from src.config import config


class AuthService():
    def __init__(self, user_serice: UserService, refresh_token_repo: RefreshTokenRepository):
        self.user_service = user_serice
        self.refresh_token_repo = refresh_token_repo

    async def get_me(self, id: str) -> User:
        return await self.user_service.get_by_id_or_raise(id)

    async def register_user(self, data: RegisterRequest) -> User:
        if await self.user_service.get_user_by_email(data.email):
            raise ValidationError("Email is already registered")
            
        if await self.user_service.get_user_by_username(data.username):
            raise ValidationError("Username is already used")

        hashed_pass = get_password_hash(data.password)
        
        payload = data.model_dump()
        payload.pop("password", None)
        payload["hashed_password"] = hashed_pass
        
        user_data = UserCreate(**payload)
        return await self.user_service.create_user(user_data)
    
    async def login(self, data: LoginRequest) -> TokenResponse:
        user = await self.user_service.get_user_by_email(data.email)
        
        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")

        access_token = create_access_token(user_id=str(user.id))
        
        refresh_token_id = uuid4()
        refresh_token = create_refresh_token(user_id=user.id, token_id=refresh_token_id)

        expires_at = datetime.now(timezone.utc) + timedelta(
            days=config.REFRESH_TOKEN_EXPIRE_DAYS
        )
        
        refresh_token_row = RefreshToken(
            id=refresh_token_id,
            user_id=user.id,
            token=refresh_token,
            expires_at=expires_at,
        )

        await self.refresh_token_repo.create(refresh_token_row)
        
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    
    async def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token)
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Refresh token expired")
        except jwt.PyJWTError:
            raise UnauthorizedError("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid refresh token")

        try:
            token_id = UUID(payload["jti"])
        except (KeyError, ValueError):
            raise UnauthorizedError("Invalid refresh token")

        token_row = await self.refresh_token_repo.get_for_update(token_id)

        if not token_row:
            raise UnauthorizedError("Invalid refresh token")

        now = datetime.now(timezone.utc)

        if token_row.revoked_at:
            raise UnauthorizedError("Refresh token expired")

        if token_row.expires_at <= now:
            raise UnauthorizedError("Refresh token expired")

        token_row.revoked_at = now

        new_token_id = uuid4()

        new_refresh_token = create_refresh_token(
            user_id=token_row.user_id,
            token_id=new_token_id,
        )

        new_row = RefreshToken(
            id=new_token_id,
            user_id=token_row.user_id,
            token=new_refresh_token,
            expires_at=now + timedelta(
                days=config.REFRESH_TOKEN_EXPIRE_DAYS
            ),
        )

        await self.refresh_token_repo.create(new_row)
        
        token_row.replaced_by = new_token_id

        return TokenResponse(
            access_token=create_access_token(user_id=token_row.user_id),
            refresh_token=new_refresh_token,
        )

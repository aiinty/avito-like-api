from src.modules.users.schemas import UserCreate
from src.modules.users.service import UserService
from src.modules.users.models import User
from src.modules.auth.schemas import TokenResponse, LoginRequest, RegisterRequest
from src.utils.security import create_access_token, create_refresh_token, get_password_hash, verify_password
from src.utils.exceptions import NotFoundError, UnauthorizedError, ValidationError
from src.utils.auth import decode_token


class AuthService():
    def __init__(self, user_serice: UserService):
        self.user_service = user_serice

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
        refresh_token = create_refresh_token(user_id=str(user.id))

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    
    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        user = decode_token(refresh_token, expected_type="refresh")

        try:
            db_user = await self.user_service.get_by_id_or_raise(user.id)
        except NotFoundError:
            raise UnauthorizedError("Invalid token")

        new_access = create_access_token(user_id=str(db_user.id))
        new_refresh = create_refresh_token(user_id=str(db_user.id))

        return TokenResponse(access_token=new_access, refresh_token=new_refresh)

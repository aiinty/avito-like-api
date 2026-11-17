from fastapi import APIRouter, Depends, status
from src.modules.auth.service import AuthService
from src.modules.auth.dependencies import get_auth_service
from src.modules.users.schemas import UserRead
from src.modules.auth.schemas import (
    RefreshRequest,
    TokenResponse,
    RegisterRequest,
    LoginRequest,
)


auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    service: AuthService = Depends(get_auth_service)
):
    return await service.register_user(data)

@auth_router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    return await service.login(data)

@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    data: RefreshRequest,
    service: AuthService = Depends(get_auth_service)
):
    return await service.refresh(data.refresh_token)

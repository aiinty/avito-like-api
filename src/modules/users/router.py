from fastapi import APIRouter, Depends
from src.modules.users.dependencies import get_user_service
from src.modules.users.service import UserService
from src.modules.users.schemas import (
    CurrentUser,
    RefreshRequest,
    TokenResponse,
    UserRegister,
    UserLogin,
    UserRead,
)
from fastapi import status
from src.utils.auth import get_current_user

users_router = APIRouter(prefix="/user", tags=["User"])

@users_router.get("/me", response_model=UserRead)
async def get_me(
    service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    return await service.get_by_id_or_raise(current_user.id)

@users_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserRegister,
    service: UserService = Depends(get_user_service)
):
    return await service.register_user(data)

@users_router.post("/login", response_model=TokenResponse)
async def login(
    data: UserLogin,
    service: UserService = Depends(get_user_service)
):
    return await service.login(data)

@users_router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    data: RefreshRequest,
    service: UserService = Depends(get_user_service)
):
    return await service.refresh_tokens(data.refresh_token)

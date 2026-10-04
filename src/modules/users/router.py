from fastapi import APIRouter, Depends, Query
from src.modules.auth.schemas import CurrentUser
from src.modules.users.dependencies import get_user_service
from src.modules.users.service import UserService
from src.modules.users.schemas import (
    UserRead,
)
from src.modules.auth.dependencies import get_current_user

users_router = APIRouter(prefix="/user", tags=["User"])

@users_router.get("/me", response_model=UserRead)
async def get_me(
    service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    return await service.get_by_id_or_raise(current_user.id)


from uuid import UUID
from fastapi import APIRouter, Depends, Query
from src.modules.items.dependencies import get_item_service
from src.modules.items.schemas import ItemRead
from src.modules.items.service import ItemService
from src.modules.auth.schemas import CurrentUser
from src.modules.users.dependencies import get_user_service
from src.modules.users.service import UserService
from src.modules.users.schemas import (
    UserRead,
    UserUpdate,
)
from src.modules.auth.dependencies import get_current_user
from src.utils.schemas import PaginatedResponse


users_router = APIRouter(prefix="/user", tags=["User"])

@users_router.get("/me", response_model=UserRead)
async def get_me(
    service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    return await service.get_by_id_or_raise(current_user.id)

@users_router.patch("/me", response_model=UserRead)
async def update_me(
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    return await service.self_update_user(current_user.id, data)

@users_router.get("/{user_id}/items", response_model=PaginatedResponse[ItemRead],)
async def get_user_items(
    user_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: ItemService = Depends(get_item_service),
) -> PaginatedResponse[ItemRead]:
    return await service.get_user_items(
        user_id=user_id,
        page=page,
        page_size=page_size,
    )

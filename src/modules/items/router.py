from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from src.modules.auth.schemas import CurrentUser
from src.modules.auth.dependencies import get_current_user
from src.modules.items.dependencies import get_item_service
from src.modules.items.schemas import ItemCreate, ItemRead, ItemUpdate
from src.modules.items.service import ItemService
from src.utils.schemas import PaginatedResponse


items_router = APIRouter(prefix="/items", tags=["Items"],)

@items_router.get("", response_model=PaginatedResponse[ItemRead])
async def get_items(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    search: Optional[str] = Query(default=None, description="Search by item title or description"),
    category_id: Optional[int] = Query(default=None),
    service: ItemService = Depends(get_item_service),
):
    return await service.get_all_items(
        page=page,
        page_size=page_size,
        search=search,
        category_id=category_id,
    )

@items_router.get("/{item_id}", response_model=ItemRead)
async def get_item(
    item_id: int,
    service: ItemService = Depends(get_item_service),
):
    return await service.get_item(item_id)

@items_router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    data: ItemCreate,
    current_user: CurrentUser = Depends(get_current_user),
    service: ItemService = Depends(get_item_service),
):
    return await service.create_item(
        author_id=current_user.id,
        data=data,
    )

@items_router.patch("/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: int,
    data: ItemUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    service: ItemService = Depends(get_item_service),
):
    return await service.update_item(
        item_id=item_id,
        user_id=current_user.id,
        data=data,
    )

@items_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    service: ItemService = Depends(get_item_service),
):
    await service.delete_item(
        item_id=item_id,
        user_id=current_user.id,
    )

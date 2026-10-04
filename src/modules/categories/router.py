from fastapi import APIRouter, Depends
from src.modules.categories.schemas import CategoryRead
from src.modules.categories.dependencies import get_categories_service
from src.modules.categories.service import CategoryService


category_router = APIRouter(prefix="/categories", tags=["Categories"])

@category_router.get("", response_model=list[CategoryRead])
async def get_categories(
    service: CategoryService = Depends(get_categories_service)
):
    return await service.get_all_categories()

@category_router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: int,
    service: CategoryService = Depends(get_categories_service)
):
    return await service.get_by_id_or_raise(category_id)

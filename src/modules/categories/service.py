from typing import List
from src.modules.categories.models import Category
from src.modules.categories.repository import CategoryRepository
from src.utils.exceptions import NotFoundError


class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def get_by_id_or_raise(
        self,
        category_id: int,
    ) -> Category:
        category = await self.repo.get_by_id(category_id)

        if not category:
            raise NotFoundError("Category not found")

        return category
    
    async def get_all_categories(self) -> List[Category]:
        return await self.repo.get_all()

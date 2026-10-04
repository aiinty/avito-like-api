from uuid import UUID
from src.modules.items.models import Item
from src.modules.items.repository import ItemRepository
from src.modules.items.schemas import ItemCreate, ItemUpdate
from src.utils.exceptions import ForbiddenError, NotFoundError
from src.utils.schemas import Meta, PaginatedResponse


class ItemService:
    def __init__(
        self,
        repo: ItemRepository,
    ):
        self.repo = repo

    async def get_by_id_or_raise(
        self,
        item_id: int,
    ) -> Item:
        item = await self.repo.get_by_id(item_id)

        if not item:
            raise NotFoundError("Item not found")

        return item

    async def _get_paginated_data(
        self,
        page: int,
        page_size: int,
        category_id: int | None = None,
        author_id: UUID | None = None,
    ) -> PaginatedResponse[Item]:
        offset = (page - 1) * page_size

        items = await self.repo.get_all(
            offset=offset,
            limit=page_size,
            category_id=category_id,
            author_id=author_id,
        )

        total_count = await self.repo.count_all(
            category_id=category_id,
            author_id=author_id,
        )

        return PaginatedResponse(
            items=items,
            meta=Meta.create(
                total_count,
                page,
                page_size,
            ),
        )

    async def get_all_items(
        self,
        page: int,
        page_size: int,
        category_id: int | None = None,
    ) -> PaginatedResponse[Item]:
        return await self._get_paginated_data(
            page=page,
            page_size=page_size,
            category_id=category_id,
        )

    async def get_item(
        self,
        item_id: int,
    ) -> Item:
        return await self.get_by_id_or_raise(item_id)

    async def get_user_items(
        self,
        user_id: UUID,
        page: int,
        page_size: int,
    ) -> PaginatedResponse[Item]:
        return await self._get_paginated_data(
            page=page,
            page_size=page_size,
            author_id=user_id,
        )

    async def create_item(
        self,
        author_id: UUID,
        data: ItemCreate,
    ) -> Item:
        return await self.repo.create(
            data=data,
            author_id=author_id,
        )

    async def update_item(
        self,
        item_id: int,
        user_id: UUID,
        data: ItemUpdate,
    ) -> Item:
        item = await self.get_by_id_or_raise(item_id)

        if item.author_id != user_id:
            raise ForbiddenError(
                "You cannot edit this item"
            )

        payload = data.model_dump(exclude_unset=True)

        return await self.repo.update(
            item,
            payload,
        )

    async def delete_item(
        self,
        item_id: int,
        user_id: UUID,
    ) -> None:
        item = await self.get_by_id_or_raise(item_id)

        if item.author_id != user_id:
            raise ForbiddenError(
                "You cannot delete this item"
            )

        await self.repo.delete(item)

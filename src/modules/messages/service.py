from uuid import UUID
from src.modules.items.repository import ItemRepository
from src.modules.messages.models import Message
from src.modules.messages.repository import MessageRepository
from src.modules.messages.schemas import MessageCreate
from src.utils.exceptions import NotFoundError
from src.utils.schemas import Meta, PaginatedResponse


class MessageService:
    def __init__(
        self,
        repo: MessageRepository,
        item_repo: ItemRepository,
    ):
        self.repo = repo
        self.item_repo = item_repo

    async def _get_item_or_raise(self, item_id: int):
        item = await self.item_repo.get_by_id(item_id)

        if not item:
            raise NotFoundError("Item not found")

        return item

    async def get_item_messages(
        self,
        item_id: int,
        page: int,
        page_size: int,
    ) -> PaginatedResponse[Message]:
        await self._get_item_or_raise(item_id)

        offset = (page - 1) * page_size

        messages = await self.repo.get_by_item_id(
            item_id=item_id,
            offset=offset,
            limit=page_size,
        )

        total_count = await self.repo.count_by_item_id(item_id)

        return PaginatedResponse(
            items=messages,
            meta=Meta.create(
                total_count,
                page,
                page_size,
            ),
        )

    async def create_message(
        self,
        item_id: int,
        user_id: UUID,
        data: MessageCreate,
    ) -> Message:
        await self._get_item_or_raise(item_id)

        return await self.repo.create(
            item_id=item_id,
            user_id=user_id,
            data=data,
        )

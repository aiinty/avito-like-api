from fastapi import APIRouter, Depends, status
from src.modules.auth.schemas import CurrentUser
from src.modules.auth.dependencies import get_current_user
from src.modules.messages.schemas import MessageCreate, MessageRead
from src.modules.messages.service import MessageService
from src.utils.schemas import PaginatedResponse
from src.modules.messages.dependencies import get_message_service


messages_router = APIRouter(prefix="/items/{item_id}/messages", tags=["Messages"])

@messages_router.get("", response_model=PaginatedResponse[MessageRead])
async def get_item_messages(
    item_id: int,
    page: int = 1,
    page_size: int = 20,
    service: MessageService = Depends(get_message_service),
):
    return await service.get_item_messages(
        item_id=item_id,
        page=page,
        page_size=page_size,
    )

@messages_router.post("", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
async def create_message(
    item_id: int,
    data: MessageCreate,
    current_user: CurrentUser = Depends(get_current_user),
    service: MessageService = Depends(get_message_service),
):
    return await service.create_message(
        item_id=item_id,
        user_id=current_user.id,
        data=data,
    )

from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.modules.items.dependencies import get_item_repo
from src.modules.items.repository import ItemRepository
from src.db.dependencies import get_postgres_session
from src.modules.messages.repository import MessageRepository
from src.modules.messages.service import MessageService

def get_messages_repo(session: AsyncSession = Depends(get_postgres_session)):
    return MessageRepository(session)

def get_message_service(
    repo: MessageRepository = Depends(get_messages_repo),
    item_repo: ItemRepository = Depends(get_item_repo)
):
    return MessageService(repo, item_repo)

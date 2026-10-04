from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.db.dependencies import get_postgres_session
from src.modules.items.repository import ItemRepository
from src.modules.items.service import ItemService

def get_item_repo(
    session: AsyncSession = Depends(get_postgres_session)
):
    return ItemRepository(session)

def get_item_service(
    repo: ItemRepository = Depends(get_item_repo)
):
    return ItemService(repo)

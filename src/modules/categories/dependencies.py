from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.db.dependencies import get_postgres_session
from src.modules.categories.repository import CategoryRepository
from src.modules.categories.service import CategoryService

def get_categories_repo(session: AsyncSession = Depends(get_postgres_session)):
    return CategoryRepository(session)

def get_categories_service(repo: CategoryRepository = Depends(get_categories_repo)):
    return CategoryService(repo)

from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.db.dependencies import get_postgres_session
from src.modules.users.repository import UserRepository
from src.modules.users.service import UserService

def get_user_repo(session: AsyncSession = Depends(get_postgres_session)):
    return UserRepository(session)

def get_user_service(repo: UserRepository = Depends(get_user_repo)):
    return UserService(repo)

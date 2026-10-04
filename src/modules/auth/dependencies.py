from uuid import UUID
import jwt
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.modules.auth.repository import RefreshTokenRepository
from src.db.dependencies import get_postgres_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.modules.auth.schemas import CurrentUser
from src.modules.auth.security import decode_token
from src.utils.exceptions import UnauthorizedError
from src.modules.auth.service import AuthService
from src.modules.users.dependencies import get_user_service
from src.modules.users.service import UserService


def get_refresh_token_repo(session: AsyncSession = Depends(get_postgres_session)):
    return RefreshTokenRepository(session)

def get_auth_service(
    user_service: UserService = Depends(get_user_service),
    refresh_repo: RefreshTokenRepository = Depends(get_refresh_token_repo)
):
    return AuthService(user_service, refresh_repo)

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> CurrentUser:
    try:
        payload = decode_token(credentials.credentials)

        if payload.get("type") != "access":
            raise UnauthorizedError("Invalid token type")

        user_id = payload.get("sub")

        if not user_id:
            raise UnauthorizedError("Invalid token payload")

        return CurrentUser(
            id=UUID(user_id)
        )

    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("Token expired")

    except (jwt.PyJWTError, ValueError):
        raise UnauthorizedError("Invalid token")

from uuid import UUID
import jwt
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.config import config
from src.utils.exceptions import ApiException, UnauthorizedError
from src.modules.users.schemas import CurrentUser

security = HTTPBearer()

def decode_token(token: str, expected_type: str) -> CurrentUser:
    try:
        payload = jwt.decode(
            token, 
            config.JWT_SECRET, 
            algorithms=[config.JWT_ALGORITHM]
        )
        if payload.get("type") != expected_type:
            raise UnauthorizedError("Invalid token type")
            
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise ApiException("Invalid token payload", status.HTTP_401_UNAUTHORIZED)
        
        return CurrentUser(
            id=UUID(user_id_str)
        )
        
    except jwt.ExpiredSignatureError:
        raise ApiException("Token expired", status.HTTP_401_UNAUTHORIZED)
    except (jwt.PyJWTError, ValueError):
        raise ApiException("Invalid token", status.HTTP_401_UNAUTHORIZED)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    return decode_token(credentials.credentials, token="access") 

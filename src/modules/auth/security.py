from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID
import bcrypt
import jwt
from src.config import config


def get_password_hash(password: str) -> str:
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=bytes, salt=salt)
    
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(
        password=password_bytes, 
        hashed_password=hashed_password_bytes
    )

def create_access_token(user_id: UUID, extra_claims: Optional[dict] = None) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    payload = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()), 
        "type": "access"
    }
    
    if extra_claims:
        payload.update(extra_claims)
    
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)

def create_refresh_token(user_id: UUID, token_id: UUID) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(
        minutes=config.REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    payload = {
        "sub": str(user_id),
        "jti": str(token_id),
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()), 
        "type": "refresh"
    }
    
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        config.JWT_SECRET,
        algorithms=[config.JWT_ALGORITHM],
    )

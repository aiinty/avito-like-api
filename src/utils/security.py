from typing import Optional
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
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
    
def create_access_token(user_id: int | str, extra_claims: Optional[dict] = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "sub": str(user_id),
        "exp": int(expire.timestamp()), 
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "type": "access"
    }
    
    if extra_claims:
        payload.update(extra_claims)
    
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)

def create_refresh_token(user_id: int | str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload = {
        "sub": str(user_id),
        "exp": int(expire.timestamp()), 
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "type": "refresh"
    }
    
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)

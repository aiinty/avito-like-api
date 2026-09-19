from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class CurrentUser(BaseModel):
    id: UUID

class RegisterRequest(BaseModel):
    email: EmailStr = Field(unique=True, max_length=255)
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(min_length=8, max_length=64)

class LoginRequest(BaseModel):
    email: str
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class RefreshRequest(BaseModel):
    refresh_token: str
    
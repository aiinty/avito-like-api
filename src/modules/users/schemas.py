from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr = Field(unique=True, max_length=255)
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    hashed_password: str = Field()
    
class UserRead(BaseModel):
    id: UUID
    username: str
    about_me: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    about_me: Optional[str] = Field(default=None, max_length=1000)
    
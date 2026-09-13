from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID
from sqlmodel import Field, Relationship, SQLModel
from src.db.fields import created_at, updated_at, uuid4_pk

if TYPE_CHECKING:
    from src.modules.items.models import Item
    from src.modules.messages.models import Message


class UserBase(SQLModel):
    email: str = Field(unique=True, max_length=255)
    username: str = Field(unique=True, max_length=32)
    about_me: Optional[str] = Field(default=None, max_length=1000)

class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: Optional[UUID] = uuid4_pk()
    hashed_password: str
    
    items: list["Item"] = Relationship(back_populates="author")
    messages: list["Message"] = Relationship(back_populates="user")
    
    created_at: Optional[datetime] = created_at()
    updated_at: Optional[datetime] = updated_at()

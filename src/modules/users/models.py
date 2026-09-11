from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID
from sqlmodel import Field, Relationship, SQLModel
from src.db.fields import created_at, updated_at, deleted_at, uuid4_pk

if TYPE_CHECKING:
    from src.modules.items.models import Item
    from src.modules.messages.models import Message


class UserBase(SQLModel):
    email: str = Field(unique=True, max_length=255)
    username: str = Field(unique=True, max_length=50)
    about_me: str | None = Field(default=None, max_length=5000)

class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: UUID | None = uuid4_pk()
    hashed_password: str
    
    items: list["Item"] = Relationship(back_populates="author")
    messages: list["Message"] = Relationship(back_populates="item")
    
    created_at: datetime | None = created_at()
    updated_at: datetime | None = updated_at()
    deleted_at: datetime | None = deleted_at()

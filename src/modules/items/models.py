import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID
from sqlmodel import Field, Relationship, SQLModel
from src.db.fields import created_at

if TYPE_CHECKING:
    from src.modules.categories.models import Category
    from src.modules.users.models import User
    from src.modules.messages.models import Message
    
    
class DealType(str, enum.Enum):
    SALE = "sale"
    FREE = "free"
    EXCHANGE = "exchange"
    
class ItemBase(SQLModel):
    title: str = Field(min_length=5, max_length=80)
    description: str = Field(min_length=10, max_length=500)
    price: int = Field(default=0, ge=0)
    photo_url: Optional[str] = Field(default=None)

class Item(ItemBase, table=True):
    __tablename__ = "items"
    
    id: Optional[int] = Field(default=None, primary_key=True) 
    deal_type: DealType = Field(default=DealType.SALE)
    category_id: int = Field(foreign_key="categories.id", index=True)
    author_id: UUID = Field(foreign_key="users.id", index=True)
    
    category: "Category" = Relationship(back_populates="items")
    author: "User" = Relationship(back_populates="items")
    messages: list["Message"] = Relationship(back_populates="item")
    
    created_at: datetime | None = created_at()

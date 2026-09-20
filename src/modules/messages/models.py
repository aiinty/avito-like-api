from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID
from sqlmodel import Field, Index, Relationship, SQLModel
from src.db.fields import created_at

if TYPE_CHECKING:
    from src.modules.items.models import Item
    from src.modules.users.models import User
    
    
class MessageBase(SQLModel):
    text: str = Field(min_length=1, max_length=500)

class Message(MessageBase, table=True):
    __tablename__ = "messages"
    
    __table_args__ = (
        Index(
            "idx_messages_item_id_id", "item_id", "id"
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="items.id", index=True, ondelete="CASCADE")
    user_id: UUID = Field(foreign_key="users.id")
    
    item: "Item" = Relationship(back_populates="messages")
    user: "User" = Relationship(back_populates="messages")
    
    created_at: datetime = created_at()

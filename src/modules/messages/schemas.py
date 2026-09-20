from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from src.modules.users.schemas import UserRead


class MessageCreate(BaseModel):
    text: str = Field(min_length=1, max_length=500)

class MessageRead(BaseModel):
    id: int
    item_id: int
    user: UserRead
    text: str
    created_at: datetime

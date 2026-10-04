import enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, model_validator
from src.modules.categories.schemas import CategoryRead
from src.modules.users.schemas import UserRead


class DealType(str, enum.Enum):
    SALE = "sale"
    FREE = "free"
    EXCHANGE = "exchange"

class ItemCreate(BaseModel):
    deal_type: DealType = Field(default=DealType.SALE)
    title: str = Field(min_length=5, max_length=80)
    description: str = Field(min_length=10, max_length=500)
    price: int = Field(default=0, ge=0)
    category_id: int = Field(ge=1)
    photo_url: Optional[str] = Field(default=None)
    
    @model_validator(mode="after")
    def check_free_price(self):
        if self.deal_type == DealType.FREE:
            self.price = 0
        return self
    
class ItemRead(BaseModel):
    id: int
    title: str
    description: str
    price: int
    deal_type: DealType
    photo_url: Optional[str]
    category: CategoryRead
    author: UserRead

class ItemUpdate(BaseModel):
    deal_type: Optional[DealType] = Field(default=None)
    title: Optional[str] = Field(default=None, min_length=5, max_length=80)
    description: Optional[str] = Field(default=None, min_length=10, max_length=500)
    price: Optional[int] = Field(default=None, ge=0)
    photo_url: Optional[str] = Field(default=None)
    category_id: Optional[int] = Field(default=None)
    
    @model_validator(mode="after")
    def check_free_price(self):
        if self.deal_type == DealType.FREE:
            self.price = 0
        return self

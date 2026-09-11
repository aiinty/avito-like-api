from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.modules.items.models import Item
    

class CategoryBase(SQLModel):
    name: str = Field(min_length=5, max_length=80)
    emoji: str = Field()

class Category(CategoryBase, table=True):
    __tablename__ = "categories"
    
    id: Optional[int] = Field(default=None, primary_key=True) 

    items: list["Item"] = Relationship(back_populates="category")
    
    
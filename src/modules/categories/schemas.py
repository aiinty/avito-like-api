from typing import Optional
from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    emoji: str = Field(min_length=1, max_length=8)

class CategoryRead(BaseModel):
    id: int
    name: str
    emoji: str

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=80)
    emoji: Optional[str] = Field(default=None, min_length=1, max_length=8)

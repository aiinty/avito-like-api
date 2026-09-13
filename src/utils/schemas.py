from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")

class Meta(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    
    @classmethod
    def create(cls, total_count: int, page: int, page_size: int) -> "Meta":
        """ Helper method to calculate pagination metadata """
        return cls(
            total=total_count,
            page=page,
            page_size=page_size,
            total_pages=(total_count + page_size - 1) // page_size if page_size > 0 else 0
        )

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    meta: Meta
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import DateTime
from src.db.fields import created_at
from sqlmodel import Field, SQLModel


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)

    user_id: UUID = Field(foreign_key="users.id", ondelete="CASCADE", index=True)
    token: str = Field(unique=True, index=True)

    expires_at: datetime = Field(sa_type=DateTime(timezone=True))
    created_at: Optional[datetime] = created_at()
    revoked_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True)
    )
    
    replaced_by: UUID | None = Field(default=None, foreign_key="refresh_tokens.id")

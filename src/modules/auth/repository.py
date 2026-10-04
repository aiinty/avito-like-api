from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.modules.auth.models import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_for_update(
        self,
        token_id: UUID,
    ) -> RefreshToken | None:

        result = await self.session.execute(
            select(RefreshToken)
            .where(RefreshToken.id == token_id)
            .with_for_update()
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        token: RefreshToken,
    ) -> RefreshToken:

        self.session.add(token)
        await self.session.flush()

        return token

    async def revoke(
        self,
        token: RefreshToken,
    ) -> None:
        token.revoked_at = datetime.now(timezone.utc)

        await self.session.flush()

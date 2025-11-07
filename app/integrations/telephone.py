from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.postgres.orm import TelephoneORM
from app.models import AddTelephone


class TelephoneRepository:
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def add_telephone(self, telephone: AddTelephone) -> TelephoneORM:
        new_telephone = TelephoneORM(
            number=telephone.number,
            company_id=telephone.company_id
        )
        self.async_session.add(new_telephone)
        await self.async_session.flush()
        await self.async_session.refresh(new_telephone)
        return new_telephone

    async def get_telephone_by_id(self, telephone_id: int) -> TelephoneORM | None:
        query = select(TelephoneORM).where(TelephoneORM.id == telephone_id)
        result = await self.async_session.execute(query)
        telephone = result.scalars().one_or_none()
        return telephone

    async def update_telephone(
        self,
        telephone_id: int,
        new_telephone: AddTelephone
    ) -> TelephoneORM | None:
        telephone = await self.async_session.get(TelephoneORM, telephone_id)
        if telephone:
            telephone.number = new_telephone.number
            telephone.company_id = new_telephone.company_id
            await self.async_session.flush()
            await self.async_session.refresh(telephone)
        return telephone

    async def delete_telephone(self, telephone_id: int) -> None:
        query = delete(TelephoneORM).where(TelephoneORM.id == telephone_id)
        await self.async_session.execute(query)
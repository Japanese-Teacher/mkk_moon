from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.integrations.postgres.orm import ActivityORM, CompanyORM
from app.models import AddCompany


class CompanyRepository:
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def add_company(self, company: AddCompany) -> CompanyORM:
        new_company = CompanyORM(
            name=company.name,
            building_id=company.building_id
        )
        if company.activity_ids:
            query = select(ActivityORM).where(ActivityORM.id.in_(company.activity_ids))
            result = await self.async_session.execute(query)
            activities = list(result.scalars().all())
            new_company.activities = activities

        self.async_session.add(new_company)
        await self.async_session.flush()
        await self.async_session.refresh(new_company)
        await self.async_session.refresh(new_company, attribute_names=["activities"])
        return new_company

    async def get_company_by_id(self, company_id: int) -> CompanyORM | None:
        query = (
            select(CompanyORM)
            .options(selectinload(CompanyORM.activities))
            .where(CompanyORM.id == company_id)
        )
        result = await self.async_session.execute(query)
        company = result.scalars().one_or_none()
        return company

    async def update_company(self, company_id: int, new_company: AddCompany) -> CompanyORM | None:
        query = (
            select(CompanyORM)
            .options(selectinload(CompanyORM.activities))
            .where(CompanyORM.id == company_id)
        )
        result = await self.async_session.execute(query)
        company = result.scalar_one_or_none()

        if company:
            company.name = new_company.name
            company.building_id = new_company.building_id

            if new_company.activity_ids:
                query = select(ActivityORM).where(ActivityORM.id.in_(new_company.activity_ids))
                result = await self.async_session.execute(query)
                activities = list(result.scalars().all())
                company.activities = activities

            await self.async_session.flush()
            await self.async_session.refresh(company, attribute_names=["activities"])

        return company

    async def delete_company(self, company_id: int) -> None:
        query = delete(CompanyORM).where(CompanyORM.id == company_id)
        await self.async_session.execute(query)
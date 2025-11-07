from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.integrations.postgres.orm import CompanyORM, ActivityORM


class FunctionalRepository:
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def get_companies_by_building_id(self, building_id: int) -> list[str]:
        query = select(CompanyORM.name).where(CompanyORM.building_id == building_id)
        result = await self.async_session.execute(query)
        return list(result.scalars().all())

    async def get_companies_by_activity_id(self, activity_id: int) -> list[str]:
        query = (
            select(CompanyORM.name)
            .join(CompanyORM.activities)
            .where(ActivityORM.id == activity_id)
        )
        result = await self.async_session.execute(query)
        return list(result.scalars().all())

    async def get_company_info_by_name(self, name: str) -> CompanyORM | None:
        query = (
            select(CompanyORM)
            .where(CompanyORM.name == name)
            .options(
                joinedload(CompanyORM.building),
                joinedload(CompanyORM.telephones),
                joinedload(CompanyORM.activities)
            )
        )
        result = await self.async_session.execute(query)
        return result.unique().scalars().one_or_none()

    async def get_company_info_by_id(self, company_id: int) -> CompanyORM | None:
        query = (
            select(CompanyORM)
            .where(CompanyORM.id == company_id)
            .options(
                joinedload(CompanyORM.building),
                joinedload(CompanyORM.telephones),
                joinedload(CompanyORM.activities)
            )
        )
        result = await self.async_session.execute(query)
        return result.unique().scalars().one_or_none()

    async def get_activity_by_name(self, name: str) -> ActivityORM | None:
        query = select(ActivityORM).where(ActivityORM.name == name)
        result = await self.async_session.execute(query)
        return result.scalars().one_or_none()

    async def get_child_activities(self, parent_id: int, max_depth: int) -> list[int]:
        query = select(ActivityORM)
        result = await self.async_session.execute(query)
        activities = result.scalars().all()

        def collect_children(pid: int):
            children = [
                activity for activity in activities
                if activity.parent_id == pid and activity.depth <= max_depth
            ]
            res = []
            for child in children:
                res.append(child.id)
                res.extend(collect_children(child.id))
            return res

        return collect_children(parent_id)

    async def get_companies_by_activities(self, activity_ids: list[int]) -> list[str]:
        query = (
            select(CompanyORM.name)
            .join(CompanyORM.activities)
            .where(ActivityORM.id.in_(activity_ids))
        )
        result = await self.async_session.execute(query)
        return list(result.scalars().unique().all())
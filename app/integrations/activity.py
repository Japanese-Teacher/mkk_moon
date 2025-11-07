from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.postgres.orm import ActivityORM
from app.models import AddActivity


class ActivityRepository:
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def add_activity(
            self,
            activity: AddActivity,
            depth: int,
    )-> ActivityORM:
        new_activity = ActivityORM(
            name=activity.name,
            parent_id=activity.parent_id,
            depth=depth,
        )
        self.async_session.add(new_activity)
        await self.async_session.flush()
        await self.async_session.refresh(new_activity)
        return new_activity

    async def get_activity_by_id(
            self,
            activity_id: int
    )-> ActivityORM:
        query = (
            select(ActivityORM)
            .where(ActivityORM.id == activity_id)
        )
        result = await self.async_session.execute(query)
        activity = result.scalars().one_or_none()
        return activity

    async def update_activity(
            self,
            activity_id: int,
            new_activity: AddActivity,
            depth: int
    )-> ActivityORM | None:
        activity = await self.async_session.get(ActivityORM, activity_id)
        if activity:
            activity.name = new_activity.name
            activity.parent_id = new_activity.parent_id
            activity.depth = depth
        await self.async_session.flush()
        await self.async_session.refresh(activity)
        return activity

    async def delete_activity(
            self,
            activity_id: int,
    )-> None:
        query = (
            delete(ActivityORM)
            .where(ActivityORM.id == activity_id)
        )
        await self.async_session.execute(query)
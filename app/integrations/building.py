from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.postgres.orm import BuildingORM
from app.models import AddBuilding


class BuildingRepository:
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def add_building(self, building: AddBuilding) -> BuildingORM:
        new_building = BuildingORM(
            address=building.address,
            latitude=building.latitude,
            longitude=building.longitude,
        )
        self.async_session.add(new_building)
        await self.async_session.flush()
        await self.async_session.refresh(new_building)
        return new_building

    async def get_building_by_id(self, building_id: int) -> BuildingORM | None:
        query = select(BuildingORM).where(BuildingORM.id == building_id)
        result = await self.async_session.execute(query)
        building = result.scalars().one_or_none()
        return building

    async def update_building(
        self,
        building_id: int,
        new_building: AddBuilding
    ) -> BuildingORM | None:
        building = await self.async_session.get(BuildingORM, building_id)
        if building:
            building.address = new_building.address
            building.latitude = new_building.latitude
            building.longitude = new_building.longitude
            await self.async_session.flush()
            await self.async_session.refresh(building)
        return building

    async def delete_building(self, building_id: int) -> None:
        query = delete(BuildingORM).where(BuildingORM.id == building_id)
        await self.async_session.execute(query)
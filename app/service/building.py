from fastapi import HTTPException

from app.integrations.building import BuildingRepository
from app.models import AddBuilding, ReadBuilding


class BuildingService:
    def __init__(self, building_repository: BuildingRepository):
        self.building_repository = building_repository

    async def add_building(self, building: AddBuilding) -> ReadBuilding:
        new_building = await self.building_repository.add_building(building)
        return ReadBuilding(
            id=new_building.id,
            address=new_building.address,
            latitude=new_building.latitude,
            longitude=new_building.longitude,
        )

    async def get_building_by_id(self, building_id: int) -> ReadBuilding:
        building = await self.building_repository.get_building_by_id(building_id)
        if not building:
            raise HTTPException(status_code=404, detail="Building not found")
        return ReadBuilding(
            id=building.id,
            address=building.address,
            latitude=building.latitude,
            longitude=building.longitude,
        )

    async def update_building(
        self,
        building_id: int,
        new_building: AddBuilding,
    ) -> ReadBuilding:
        updated_building = await self.building_repository.update_building(building_id, new_building)
        if not updated_building:
            raise HTTPException(status_code=404, detail="Building not found")
        return ReadBuilding(
            id=updated_building.id,
            address=updated_building.address,
            latitude=updated_building.latitude,
            longitude=updated_building.longitude,
        )

    async def delete_building(self, building_id: int) -> None:
        building = await self.building_repository.get_building_by_id(building_id)
        if not building:
            raise HTTPException(status_code=404, detail="Building not found")
        await self.building_repository.delete_building(building_id)
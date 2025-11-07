from typing import Annotated

from fastapi import Depends, APIRouter

from app.models import ReadBuilding, AddBuilding
from app.service.building import BuildingService
from app.service.depends.dependencies import get_building_service

building_router = APIRouter(prefix="/buildings", tags=["buildings"])

@building_router.post('', response_model=ReadBuilding)
async def add_building(
    building_service: Annotated[BuildingService, Depends(get_building_service)],
    building: AddBuilding,
) -> ReadBuilding:
    return await building_service.add_building(building)

@building_router.get('/{building_id}', response_model=ReadBuilding)
async def get_building_by_id(
    building_service: Annotated[BuildingService, Depends(get_building_service)],
    building_id: int,
) -> ReadBuilding:
    return await building_service.get_building_by_id(building_id)

@building_router.put('/{building_id}', response_model=ReadBuilding)
async def update_building(
    building_service: Annotated[BuildingService, Depends(get_building_service)],
    building_id: int,
    new_building: AddBuilding,
) -> ReadBuilding:
    return await building_service.update_building(building_id, new_building)

@building_router.delete('/{building_id}', status_code=204)
async def delete_building(
    building_service: Annotated[BuildingService, Depends(get_building_service)],
    building_id: int,
) -> None:
    await building_service.delete_building(building_id)
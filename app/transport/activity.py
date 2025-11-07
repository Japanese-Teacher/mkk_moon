from typing import Annotated

from fastapi import APIRouter, Depends

from app.models import ReadActivity, AddActivity
from app.service.activity import ActivityService
from app.service.depends.dependencies import get_activity_service

activity_router = APIRouter(prefix="/activities", tags=["activities"])

@activity_router.post('', response_model=ReadActivity)
async def add_activity(
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
    activity: AddActivity,
) -> ReadActivity:
    return await activity_service.add_activity(activity)

@activity_router.get('/{activity_id}', response_model=ReadActivity)
async def get_activity_by_id(
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
    activity_id: int,
) -> ReadActivity:
    return await activity_service.get_activity_by_id(activity_id)

@activity_router.put('/{activity_id}', response_model=ReadActivity)
async def update_activity(
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
    activity_id: int,
    new_activity: AddActivity,
) -> ReadActivity:
    return await activity_service.update_activity(activity_id, new_activity)

@activity_router.delete('/{activity_id}', status_code=204)
async def delete_activity(
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
    activity_id: int,
) -> None:
    await activity_service.delete_activity(activity_id)
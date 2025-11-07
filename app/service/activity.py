from fastapi import HTTPException

from app.integrations.activity import ActivityRepository
from app.models import AddActivity, ReadActivity


class ActivityService:
    def __init__(self, activity_repository: ActivityRepository):
        self.activity_repository = activity_repository

    async def _get_depth(self, parent_id: int | None) -> int:
        if parent_id is None:
            return 1

        parent = await self.activity_repository.get_activity_by_id(parent_id)
        if not parent:
            raise HTTPException(404, "Parent activity not found")

        depth = parent.depth + 1
        if depth > 3:
            raise HTTPException(400, "Max depth is 3 levels")
        return depth

    async def add_activity(self, activity: AddActivity) -> ReadActivity:
        depth = await self._get_depth(activity.parent_id)
        new_activity = await self.activity_repository.add_activity(activity, depth)
        return ReadActivity.model_validate(new_activity)

    async def get_activity_by_id(self, activity_id: int) -> ReadActivity:
        activity = await self.activity_repository.get_activity_by_id(activity_id)
        if not activity:
            raise HTTPException(404, "Activity not found")
        return ReadActivity.model_validate(activity)

    async def update_activity(
            self,
            activity_id: int,
            new_activity: AddActivity,
    ) -> ReadActivity:
        existing_activity = await self.activity_repository.get_activity_by_id(activity_id)
        if not existing_activity:
            raise HTTPException(404, "Activity not found")

        depth = await self._get_depth(new_activity.parent_id)
        updated_activity = await self.activity_repository.update_activity(
            activity_id,
            new_activity,
            depth
        )
        return ReadActivity.model_validate(updated_activity)

    async def delete_activity(self, activity_id: int) -> None:
        activity = await self.activity_repository.get_activity_by_id(activity_id)
        if not activity:
            raise HTTPException(404, "Activity not found")

        await self.activity_repository.delete_activity(activity_id)

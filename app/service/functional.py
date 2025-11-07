from fastapi import HTTPException

from app.integrations.functional import FunctionalRepository
from app.models import GetCompany


class FunctionalService:
    def __init__(self, functional_repository: FunctionalRepository):
        self.functional_repository = functional_repository

    async def get_companies_by_building_id(self, building_id: int) -> list[str]:
        return await self.functional_repository.get_companies_by_building_id(building_id)

    async def get_companies_by_activity_id(self, activity_id: int) -> list[str]:
        return await self.functional_repository.get_companies_by_activity_id(activity_id)

    async def get_company_info_by_name(self, name: str) -> GetCompany:
        company = await self.functional_repository.get_company_info_by_name(name)

        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        return GetCompany(
            id=company.id,
            name=company.name,
            telephone_numbers=[telephone.number for telephone in company.telephones],
            building=company.building.address,
            activities=[activity.name for activity in company.activities]
        )

    async def get_company_info_by_id(self, company_id: int) -> GetCompany:
        company = await self.functional_repository.get_company_info_by_id(company_id)

        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        return GetCompany(
            id=company_id,
            name=company.name,
            telephone_numbers=[telephone.number for telephone in company.telephones],
            building=company.building.address,
            activities=[activity.name for activity in company.activities]
        )

    async def get_companies_by_activity_name(self, activity_name: str) -> list[str]:
        root = await self.functional_repository.get_activity_by_name(activity_name)
        if not root:
            raise HTTPException(status_code=404, detail="Activity not found")

        max_depth = 3
        children_ids = await self.functional_repository.get_child_activities(
            root.id, max_depth
        )

        activity_ids = [root.id] + children_ids
        return await self.functional_repository.get_companies_by_activities(activity_ids)
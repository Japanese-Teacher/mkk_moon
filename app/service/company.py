from fastapi import HTTPException

from app.integrations.company import CompanyRepository
from app.models import ReadCompany, AddCompany


class CompanyService:
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    async def add_company(self, company: AddCompany) -> ReadCompany:
        new_company = await self.company_repository.add_company(company)
        activity_ids = [activity.id for activity in new_company.activities]
        return ReadCompany(
            id=new_company.id,
            name=new_company.name,
            building_id=new_company.building_id,
            activity_ids=activity_ids
        )

    async def get_company_by_id(self, company_id: int) -> ReadCompany:
        company = await self.company_repository.get_company_by_id(company_id)

        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        activity_ids = [activity.id for activity in company.activities]
        return ReadCompany(
            id=company.id,
            name=company.name,
            building_id=company.building_id,
            activity_ids=activity_ids
        )

    async def update_company(self, company_id: int, new_company: AddCompany) -> ReadCompany:
        updated_company = await self.company_repository.update_company(company_id, new_company)

        if not updated_company:
            raise HTTPException(status_code=404, detail="Company not found")

        activity_ids = [activity.id for activity in updated_company.activities]
        return ReadCompany(
            id=updated_company.id,
            name=updated_company.name,
            building_id=updated_company.building_id,
            activity_ids=activity_ids
        )

    async def delete_company(self, company_id: int) -> None:
        company = await self.company_repository.get_company_by_id(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        await self.company_repository.delete_company(company_id)
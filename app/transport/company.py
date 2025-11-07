from typing import Annotated

from fastapi import APIRouter, Depends

from app.models import ReadCompany, AddCompany
from app.service.company import CompanyService
from app.service.depends.dependencies import get_company_service

company_router = APIRouter(prefix='/companies', tags=['Companies'])

@company_router.post('', response_model=ReadCompany)
async def add_company(
    company_service: Annotated[CompanyService, Depends(get_company_service)],
    company: AddCompany,
) -> ReadCompany:
    return await company_service.add_company(company)

@company_router.get('/{company_id}', response_model=ReadCompany)
async def get_company_by_id(
    company_service: Annotated[CompanyService, Depends(get_company_service)],
    company_id: int,
) -> ReadCompany:
    return await company_service.get_company_by_id(company_id)

@company_router.put('/{company_id}', response_model=ReadCompany)
async def update_company(
    company_service: Annotated[CompanyService, Depends(get_company_service)],
    company_id: int,
    new_company: AddCompany,
) -> ReadCompany:
    return await company_service.update_company(company_id, new_company)

@company_router.delete('/{company_id}', status_code=204)
async def delete_company(
    company_service: Annotated[CompanyService, Depends(get_company_service)],
    company_id: int,
) -> None:
    await company_service.delete_company(company_id)

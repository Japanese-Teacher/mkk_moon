from typing import Annotated

from fastapi import Depends, APIRouter

from app.models import GetCompany
from app.service.depends.dependencies import get_functional_service
from app.service.functional import FunctionalService

functional_router = APIRouter(prefix='/functional', tags=['Functional'])

@functional_router.get('/buildings/{building_id}/companies', response_model=list[str])
async def get_companies_by_building_id(
    functional_service: Annotated[FunctionalService, Depends(get_functional_service)],
    building_id: int,
) -> list[str]:
    return await functional_service.get_companies_by_building_id(building_id)

@functional_router.get('/activities/{activity_id}/companies', response_model=list[str])
async def get_companies_by_activity_id(
    functional_service: Annotated[FunctionalService, Depends(get_functional_service)],
    activity_id: int,
) -> list[str]:
    return await functional_service.get_companies_by_activity_id(activity_id)

@functional_router.get("/companies/by-name", response_model=GetCompany)
async def get_company_info_by_name(
    functional_service: Annotated[FunctionalService, Depends(get_functional_service)],
    name: str,
) -> GetCompany:
    return await functional_service.get_company_info_by_name(name)

@functional_router.get("/companies/{company_id}", response_model=GetCompany)
async def get_company_info_by_id(
    functional_service: Annotated[FunctionalService, Depends(get_functional_service)],
    company_id: int,
) -> GetCompany:
    return await functional_service.get_company_info_by_id(company_id)

@functional_router.get('/companies', response_model=list[str])
async def get_companies_by_activity_name(
    functional_service: Annotated[FunctionalService, Depends(get_functional_service)],
    activity_name: str,
) -> list[str]:
    return await functional_service.get_companies_by_activity_name(activity_name)
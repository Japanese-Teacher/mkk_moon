from typing import Annotated

from fastapi import Depends

from app.integrations.activity import ActivityRepository
from app.integrations.building import BuildingRepository
from app.integrations.company import CompanyRepository
from app.integrations.depends.dependencies import get_company_repository, get_activity_repository, \
    get_building_repository, get_telephone_repository, get_functional_repository
from app.integrations.functional import FunctionalRepository
from app.integrations.telephone import TelephoneRepository
from app.service.activity import ActivityService
from app.service.building import BuildingService
from app.service.company import CompanyService
from app.service.functional import FunctionalService
from app.service.telephone import TelephoneService


async def get_company_service(
    company_repository: Annotated[CompanyRepository, Depends(get_company_repository)]
) -> CompanyService:
    return CompanyService(company_repository)

async def get_activity_service(
    activity_repository: Annotated[ActivityRepository, Depends(get_activity_repository)]
) -> ActivityService:
    return ActivityService(activity_repository)

async def get_building_service(
    building_repository: Annotated[BuildingRepository, Depends(get_building_repository)]
) -> BuildingService:
    return BuildingService(building_repository)

async def get_telephone_service(
    telephone_repository: Annotated[TelephoneRepository, Depends(get_telephone_repository)]
) -> TelephoneService:
    return TelephoneService(telephone_repository)

async def get_functional_service(
    functional_repository: Annotated[FunctionalRepository, Depends(get_functional_repository)]
) -> FunctionalService:
    return FunctionalService(functional_repository)
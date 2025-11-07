from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.activity import ActivityRepository
from app.integrations.building import BuildingRepository
from app.integrations.company import CompanyRepository
from app.integrations.functional import FunctionalRepository
from app.integrations.telephone import TelephoneRepository
from app.transport.depends.db import get_async_session


async def get_company_repository(
        async_session: Annotated[AsyncSession, Depends(get_async_session)]
) -> CompanyRepository:
    return CompanyRepository(async_session)


async def get_activity_repository(
        async_session: Annotated[AsyncSession, Depends(get_async_session)]
) -> ActivityRepository:
    return ActivityRepository(async_session)


async def get_building_repository(
        async_session: Annotated[AsyncSession, Depends(get_async_session)]
) -> BuildingRepository:
    return BuildingRepository(async_session)


async def get_telephone_repository(
        async_session: Annotated[AsyncSession, Depends(get_async_session)]
) -> TelephoneRepository:
    return TelephoneRepository(async_session)


async def get_functional_repository(
        async_session: Annotated[AsyncSession, Depends(get_async_session)]
) -> FunctionalRepository:
    return FunctionalRepository(async_session)

from typing import Annotated

from fastapi import APIRouter, Depends

from app.models import ReadTelephone, AddTelephone
from app.service.depends.dependencies import get_telephone_service
from app.service.telephone import TelephoneService

telephone_router = APIRouter(prefix='/telephones', tags=['Telephones'])

@telephone_router.post('', response_model=ReadTelephone)
async def add_telephone(
    telephone_service: Annotated[TelephoneService, Depends(get_telephone_service)],
    telephone: AddTelephone,
) -> ReadTelephone:
    return await telephone_service.add_telephone(telephone)

@telephone_router.get('/{telephone_id}', response_model=ReadTelephone)
async def get_telephone_by_id(
    telephone_service: Annotated[TelephoneService, Depends(get_telephone_service)],
    telephone_id: int,
) -> ReadTelephone:
    return await telephone_service.get_telephone_by_id(telephone_id)

@telephone_router.put('/{telephone_id}', response_model=ReadTelephone)
async def update_telephone(
    telephone_service: Annotated[TelephoneService, Depends(get_telephone_service)],
    telephone_id: int,
    new_telephone: AddTelephone,
) -> ReadTelephone:
    return await telephone_service.update_telephone(telephone_id, new_telephone)

@telephone_router.delete('/{telephone_id}', status_code=204)
async def delete_telephone(
    telephone_service: Annotated[TelephoneService, Depends(get_telephone_service)],
    telephone_id: int,
) -> None:
    await telephone_service.delete_telephone(telephone_id)
from fastapi import HTTPException

from app.integrations.telephone import TelephoneRepository
from app.models import AddTelephone, ReadTelephone


class TelephoneService:
    def __init__(self, telephone_repository: TelephoneRepository):
        self.telephone_repository = telephone_repository

    async def add_telephone(self, telephone: AddTelephone) -> ReadTelephone:
        new_telephone = await self.telephone_repository.add_telephone(telephone)
        return ReadTelephone.model_validate(new_telephone)

    async def get_telephone_by_id(self, telephone_id: int) -> ReadTelephone:
        telephone = await self.telephone_repository.get_telephone_by_id(telephone_id)
        if not telephone:
            raise HTTPException(status_code=404, detail="Telephone not found")
        return ReadTelephone.model_validate(telephone)

    async def update_telephone(
        self,
        telephone_id: int,
        new_telephone: AddTelephone,
    ) -> ReadTelephone:
        updated_telephone = await self.telephone_repository.update_telephone(
            telephone_id, new_telephone
        )
        if not updated_telephone:
            raise HTTPException(status_code=404, detail="Telephone not found")
        return ReadTelephone.model_validate(updated_telephone)

    async def delete_telephone(self, telephone_id: int) -> None:
        telephone = await self.telephone_repository.get_telephone_by_id(telephone_id)
        if not telephone:
            raise HTTPException(status_code=404, detail="Telephone not found")
        await self.telephone_repository.delete_telephone(telephone_id)
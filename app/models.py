from pydantic import BaseModel, ConfigDict


class AddTelephone(BaseModel):
    number: str
    company_id: int


class ReadTelephone(BaseModel):
    id: int
    number: str
    company_id: int

    model_config = ConfigDict(from_attributes=True)


class AddActivity(BaseModel):
    name: str
    parent_id: int | None = None


class ReadActivity(BaseModel):
    id: int
    name: str
    parent_id: int | None = None
    depth: int

    model_config = ConfigDict(from_attributes=True)


class AddBuilding(BaseModel):
    address: str
    latitude: float
    longitude: float


class ReadBuilding(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)


class AddCompany(BaseModel):
    name: str
    building_id: int
    activity_ids: list[int]


class ReadCompany(BaseModel):
    id: int
    name: str
    building_id: int
    activity_ids: list[int]

    model_config = ConfigDict(from_attributes=True)


class GetCompany(BaseModel):
    id: int
    name: str
    telephone_numbers: list[str]
    building: str
    activities: list[str]

    model_config = ConfigDict(from_attributes=True)

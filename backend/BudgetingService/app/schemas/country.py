import uuid
from pydantic import BaseModel


class CountryBase(BaseModel):
    country: str
    currency: str
    phone_code: str


class CountryCreate(CountryBase):
    pass


class CountryResponse(CountryBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
